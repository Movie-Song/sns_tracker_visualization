import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from notion_api import get_dataframe  # 기존의 get_dataframe() 사용

st.title("지난 365일 깃허브 잔디 스타일 시각화")

# 1) Notion에서 데이터 가져오기 (df_user)
#    df_user는 날짜(Date)를 인덱스로 하고, "Count" 컬럼이 있는 형태로 가정
df_user = get_dataframe()

# 데이터가 없으면 중단
if df_user.empty:
    st.error("데이터가 없습니다. Notion API 설정 또는 DATABASE_ID를 확인해 주세요.")
    st.stop()

# 2) 365일 범위 날짜 생성
end_date = pd.to_datetime("today").normalize()   # 오늘 날짜(시분초=00:00:00)
start_date = end_date - pd.Timedelta(days=364)   # 365일 전 (오늘 포함)

date_range = pd.date_range(start=start_date, end=end_date, freq="D")

# 3) 날짜 범위 전체를 담는 달력용 DataFrame 생성 (기본 Count=0)
df_calendar = pd.DataFrame(index=date_range)
df_calendar["Date"] = df_calendar.index
df_calendar["Count"] = 0

# 4) 실제 데이터(df_user)로 Count 값 채우기
#    df_user.index가 2024-08-16 같은 datetime 형식이라고 가정
for date_i, row in df_user.iterrows():
    if date_i in df_calendar.index:
        df_calendar.loc[date_i, "Count"] = row["Count"]

# 5) 요일(Weekday)와 주(WeekIndex) 계산
#    weekday(): 0=월, 6=일
df_calendar["Weekday"] = df_calendar.index.weekday
df_calendar["WeekIndex"] = ((df_calendar.index - start_date).days // 7).astype(int)

# 6) 피벗 테이블 (행=요일, 열=주차)
pivot = df_calendar.pivot(index="Weekday", columns="WeekIndex", values="Count")

st.subheader("피벗 테이블")
st.write(pivot)

# 7) 히트맵 시각화
fig, ax = plt.subplots(figsize=(16, 3))

heatmap = ax.pcolormesh(pivot, cmap="Greens", edgecolors="white")
plt.colorbar(heatmap, ax=ax)

# X축: 주차
ax.set_xticks(np.arange(pivot.shape[1]) + 0.5)
ax.set_xticklabels(pivot.columns, rotation=90)

# Y축: 요일 (0=월, 6=일)
ax.set_yticks(np.arange(7) + 0.5)
ax.set_yticklabels(["월", "화", "수", "목", "금", "토", "일"])

ax.set_xlabel("WeekIndex (0 = 365일 전 주)")
ax.set_ylabel("요일")
ax.set_title("지난 365일 Contributions Heatmap")

st.pyplot(fig)
