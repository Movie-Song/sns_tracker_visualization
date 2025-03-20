import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from notion_api import get_dataframe

st.title("Notion 데이터 깃허브 잔디 스타일 시각화")

st.write("Hello, world!")

# Notion 데이터를 DataFrame 형태로 가져옵니다.
df = get_dataframe()

# 데이터가 없을 경우 메시지를 출력하고 종료합니다.
if df.empty:
    st.error("데이터가 없습니다. Notion API 설정과 DATABASE_ID를 확인해 주세요.")
    st.stop()

# 원본 데이터를 확인할 수 있도록 출력합니다.
st.subheader("가져온 데이터")
st.write(df)

# 날짜별 데이터를 주차(Week)와 요일(Weekday)로 분리하여 히트맵에 사용할 pivot 테이블을 만듭니다.
df["Weekday"] = df.index.weekday  # 0: 월요일, 6: 일요일
df["Week"] = df.index.isocalendar().week  # ISO 주 번호

pivot = df.pivot_table(values="Count", index="Weekday", columns="Week", fill_value=0)

# 히트맵을 생성합니다.
fig, ax = plt.subplots(figsize=(12, 4))
heatmap = ax.pcolormesh(pivot, cmap="Greens", edgecolors="gray")
plt.colorbar(heatmap, ax=ax)

# 축 레이블 설정
ax.set_xticks(np.arange(len(pivot.columns)) + 0.5)
ax.set_xticklabels(pivot.columns, rotation=90)
ax.set_yticks(np.arange(7) + 0.5)
ax.set_yticklabels(["월", "화", "수", "목", "금", "토", "일"])
ax.set_xlabel("주차")
ax.set_ylabel("요일")
ax.set_title("Notion 데이터 Contributions Heatmap")

st.pyplot(fig)
