import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime, timedelta
from notion_api import get_dataframe

# Notion API에서 데이터 가져오기
df_user = get_dataframe()

if df_user.empty:
    st.error("데이터가 없습니다. Notion API 설정과 DATABASE_ID를 확인해 주세요.")
    st.stop()

# 오늘 기준 지난 365일 날짜 범위 생성 (오늘 포함)
end_date = pd.to_datetime("today").normalize()
start_date = end_date - pd.Timedelta(days=364)
date_range = pd.date_range(start=start_date, end=end_date, freq="D")

# 달력용 DataFrame 생성 (기본 Count = 0)
df_calendar = pd.DataFrame(index=date_range)
df_calendar["Count"] = 0

# Notion 데이터(df_user)의 Count를 달력 DataFrame에 반영 (날짜가 일치하는 경우)
for date_i, row in df_user.iterrows():
    if date_i in df_calendar.index:
        df_calendar.loc[date_i, "Count"] = row["Count"]

# 요일(Weekday)와 주(WeekIndex) 계산
df_calendar["Weekday"] = df_calendar.index.weekday           # 0: 월요일, 6: 일요일
df_calendar["WeekIndex"] = ((df_calendar.index - start_date).days // 7).astype(int)

# 피벗 테이블 생성 (행=요일, 열=주차, 값=Count)
pivot = df_calendar.pivot(index="Weekday", columns="WeekIndex", values="Count")
# Count 값이 5보다 크면 5로 클리핑
pivot = pivot.clip(upper=5)

# 사용자 지정 색상 설정 (0~5)
# 0: #F2F2F2 (옅은 회색), 1: #FCFEB3, 2: #C6EA74, 3: #68CB57, 4: #00893E, 5: #006B31
colors = ["#F2F2F2", "#FCFEB3", "#C6EA74", "#68CB57", "#00893E", "#006B31"]
cmap = mcolors.ListedColormap(colors)
# 경계값: 0,1,2,3,4,5,6 → 각 구간에 맞게 색상 적용
boundaries = [0, 1, 2, 3, 4, 5, 6]
norm = mcolors.BoundaryNorm(boundaries, ncolors=cmap.N)

# 히트맵 그리기 (불필요한 축, 눈금, 범례, 제목 제거)
fig, ax = plt.subplots(figsize=(16, 3))
ax.pcolormesh(pivot, cmap=cmap, norm=norm, edgecolors="white")
ax.axis("off")  # 축 및 눈금 제거

st.pyplot(fig)
