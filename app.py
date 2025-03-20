import streamlit as st
import pandas as pd  # ✅ pandas 가져오기 (중요)
import matplotlib.pyplot as plt
import numpy as np
from notion_api import get_dataframe  # 노션 API 모듈 불러오기

# ✅ get_dataframe()이 실행되는지 확인
st.write("✅ get_dataframe() 호출됨")

# ✅ 데이터 가져오기
df = get_dataframe()

# ✅ 데이터 타입 확인
st.write("📊 데이터 타입:", type(df))

# ✅ pandas 객체인지 확인
if isinstance(df, pd.DataFrame):
    st.write("✅ `df`는 pandas DataFrame입니다.")
else:
    st.error(f"🚨 `df`가 DataFrame이 아닙니다. 현재 타입: {type(df)}")

# ✅ df가 비어 있으면 경고 메시지 출력
if df is None:
    st.error("🚨 `get_dataframe()`이 `None`을 반환했습니다. 확인이 필요합니다!")
elif df.empty:
    st.warning("⚠️ 데이터가 없습니다. 노션 API 응답을 확인하세요!")
else:
    st.write("📊 가져온 데이터:", df)


if df is None:
    st.error("🚨 `get_dataframe()`이 `None`을 반환했습니다. 확인이 필요합니다!")
elif df.empty:
    st.warning("⚠️ 데이터가 없습니다. 노션 API 응답을 확인하세요!")
else:
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
