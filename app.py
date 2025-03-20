import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from notion_api import get_dataframe  # 노션 API 모듈 불러오기

# 데이터 가져오기
df = get_dataframe()

# 데이터 가공
df["Weekday"] = df.index.weekday  # 요일 (0: 월, 6: 일)
df["Week"] = df.index.isocalendar().week  # 몇 번째 주인지
pivot_table = df.pivot_table(values="Count", index="Weekday", columns="Week", fill_value=0)

# Streamlit UI
st.title("노션 데이터 깃허브 잔디 스타일 시각화")

fig, ax = plt.subplots(figsize=(12, 4))
heatmap = plt.pcolormesh(pivot_table, cmap="Greens", edgecolors="gray")
plt.colorbar(heatmap)
plt.xticks(rotation=90)
plt.yticks(np.arange(7) + 0.5, ["월", "화", "수", "목", "금", "토", "일"])
plt.title("깃허브 잔디 스타일 히트맵")

st.pyplot(fig)
