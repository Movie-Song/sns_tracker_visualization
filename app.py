import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from notion_api import get_dataframe  # 노션 API 모듈 불러오기

# ✅ 데이터 가져오기
df = get_dataframe()

# ✅ 데이터가 비어 있으면 경고 메시지 출력
if df.empty:
    st.warning("⚠️ 데이터가 없습니다. 노션 API 응답을 확인하세요!")
else:
    st.write("📊 가져온 데이터:", df)

# ✅ 데이터 확인
st.write("📊 가져온 데이터:", df)

# ✅ 데이터 정보 출력 (디버깅용)
st.write("📊 데이터프레임 정보:", df.info())
st.write("📊 가져온 데이터:", df)

# ✅ 날짜 변환 (주차 & 요일 추가)
df["Weekday"] = df.index.weekday  # 요일 (0=월요일, 6=일요일)
df["Week"] = df.index.isocalendar().week  # 몇 번째 주인지

# ✅ pivot_table 수정 (값이 없을 때 0으로 채우기)
pivot_table = df.pivot_table(values="Count", index="Weekday", columns="Week", fill_value=0)

# Streamlit UI
st.title("노션 데이터 깃허브 잔디 스타일 시각화")

fig, ax = plt.subplots(figsize=(12, 4))
heatmap = plt.pcolormesh(pivot_table, cmap="Greens", edgecolors="gray")
plt.colorbar(heatmap)

# ✅ 축 레이블 추가
ax.set_xticks(np.arange(len(pivot_table.columns)) + 0.5)
ax.set_xticklabels(pivot_table.columns, rotation=90)
ax.set_yticks(np.arange(7) + 0.5)
ax.set_yticklabels(["월", "화", "수", "목", "금", "토", "일"])

plt.xlabel("주차")
plt.ylabel("요일")
plt.title("노션 데이터 깃허브 잔디 스타일 시각화")

st.pyplot(fig)
