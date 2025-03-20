import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime, timedelta

from notion_api import get_dataframe  # 기존 get_dataframe() 그대로 사용

# 1) Notion에서 데이터 가져오기
df_user = get_dataframe()

# 데이터가 없으면 앱 종료
if df_user.empty:
    st.stop()

# 2) 지난 365일 날짜 범위 생성
end_date = pd.to_datetime("today").normalize()   # 오늘 (날짜만)
start_date = end_date - pd.Timedelta(days=364)   # 364일 전 → 총 365일

date_range = pd.date_range(start=start_date, end=end_date, freq="D")

# 3) 달력용 DataFrame (기본 Count=0)
df_calendar = pd.DataFrame(index=date_range)
df_calendar["Count"] = 0

# 4) 실제 사용자 데이터(df_user)로부터 Count 대입
for date_i, row in df_user.iterrows():
    if date_i in df_calendar.index:
        df_calendar.loc[date_i, "Count"] = row["Count"]

# 5) 요일(Weekday), 주차(WeekIndex) 계산
df_calendar["Weekday"] = df_calendar.index.weekday           # 0=월, 6=일
df_calendar["WeekIndex"] = ((df_calendar.index - start_date).days // 7).astype(int)

# 6) 피벗 테이블: (행=요일, 열=주차)
pivot = df_calendar.pivot(index="Weekday", columns="WeekIndex", values="Count")

# 7) 색상 단계 설정 (0~5 구간)
#   - ListedColormap + BoundaryNorm 이용 → 6단계(0=흰색, 5=가장 진한 색)
colors = ["white", "#e6ffe6", "#b3ffb3", "#80ff80", "#4dff4d", "#00cc00"]
cmap = mcolors.ListedColormap(colors)
boundaries = [0, 1, 2, 3, 4, 5, 999]  # 마지막 구간(5 이상)은 전부 최대치 색상

norm = mcolors.BoundaryNorm(boundaries, ncolors=cmap.N)

# 8) 히트맵 그리기
fig, ax = plt.subplots(figsize=(16, 3))
heatmap = ax.pcolormesh(pivot, cmap=cmap, norm=norm, edgecolors="white")
plt.colorbar(heatmap, ax=ax)

# 축 설정
ax.set_xticks(np.arange(pivot.shape[1]) + 0.5)
ax.set_xticklabels(pivot.columns, rotation=90)
ax.set_yticks(np.arange(7) + 0.5)
ax.set_yticklabels(["월", "화", "수", "목", "금", "토", "일"])

ax.set_title("지난 365일 Contributions Heatmap")

# 9) 최종 이미지 출력 (임베드 시 히트맵만 보이도록)
st.pyplot(fig)
