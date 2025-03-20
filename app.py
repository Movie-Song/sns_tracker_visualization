import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from notion_api import get_dataframe  # 노션 API 모듈 불러오기

# 데이터 가져오기
df = get_dataframe()

# ✅ 데이터를 출력하여 확인
st.write("📊 가져온 데이터:", df)
