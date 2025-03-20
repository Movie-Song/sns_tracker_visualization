import streamlit as st
import pandas as pd  # ✅ pandas 가져오기
import matplotlib.pyplot as plt
import numpy as np
from notion_api import get_dataframe  # 노션 API 모듈 불러오기

st.title("📊 노션 데이터 시각화")

# ✅ get_dataframe()이 실행되는지 확인
st.write("✅ `get_dataframe()` 호출됨")

# ✅ 데이터 가져오기
df = get_dataframe()

# ✅ 강제 출력: `df` 값 직접 확인
st.write("📌 `df`의 원본 값:", df)

# ✅ `df`가 None인지 확인
if df is None:
    st.error("🚨 `df`가 `None`입니다. Notion API 응답을 확인하세요!")
    st.stop()

# ✅ `df`가 비어 있는지 확인
if df.empty:
    st.warning("⚠️ 데이터가 없습니다. 노션 API 응답을 확인하세요!")
    st.stop()

# ✅ `df`가 pandas DataFrame인지 체크
if not isinstance(df, pd.DataFrame):
    st.error(f"🚨 `df`의 타입이 이상합니다! 현재 타입: {type(df)}")
    st.stop()

# ✅ index 변환이 가능한지 확인
st.write("📌 `df.index` 값:", df.index)

try:
    df["Weekday"] = df.index.weekday  # 요일 (0=월요일, 6=일요일)
    df["Week"] = df.index.isocalendar().week
    st.success("✅ 요일 및 주차 데이터 생성 완료")
except Exception as e:
    st.error(f"🚨 `df.index.weekday` 변환 중 오류 발생: {e}")
    st.stop()

# ✅ 시각화 코드 유지
fig, ax = plt.subplots(figsize=(12, 4))
pivot_table = df.pivot_table(values="Count", index="Weekday", columns="Week", fill_value=0)
heatmap = plt.pcolormesh(pivot_table, cmap="Greens", edgecolors="gray")
plt.colorbar(heatmap)
ax.set_xticks(np.arange(len(pivot_table.columns)) + 0.5)
ax.set_xticklabels(pivot_table.columns, rotation=90)
ax.set_yticks(np.arange(7) + 0.5)
ax.set_yticklabels(["월", "화", "수", "목", "금", "토", "일"])
plt.xlabel("주차")
plt.ylabel("요일")
plt.title("노션 데이터 깃허브 잔디 스타일 시각화")
st.pyplot(fig)
