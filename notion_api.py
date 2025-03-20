import os
import requests
import pandas as pd
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime, timedelta

# 환경 변수 로드
load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_notion_data():
    print("✅ get_notion_data() 실행됨")

    one_year_ago = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"filter": {"property": "Date", "date": {"after": one_year_ago}}}
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # ✅ API 응답 직접 출력
    print("📌 Notion API 응답:", data)

    if "results" not in data:
        print("🚨 Notion API 응답에 `results` 키가 없음!", data)
        return {}

    return data

def extract_dates(data):
    """ 날짜별 카운트 집계 """
    date_counts = defaultdict(int)

    for item in data.get("results", []):
        properties = item.get("properties", {})

        # ✅ Date 필드 확인
        date_property = properties.get("Date", {}).get("date", {})
        print("📅 가져온 날짜 데이터:", date_property)  # 디버깅 출력

        if "start" in date_property:
            raw_date = date_property["start"]
            formatted_date = datetime.fromisoformat(raw_date[:10]).strftime("%Y-%m-%d")
            date_counts[formatted_date] += 1

    print("📊 변환된 날짜별 데이터 카운트:", date_counts)  # 디버깅 출력
    return date_counts

def get_dataframe():
    """ 데이터프레임 변환 """
    print("✅ get_dataframe() 실행됨")  # 함수 실행 확인

    notion_data = get_notion_data()

    if "results" not in notion_data:
        print("⚠️ API에서 데이터를 가져오지 못함!", notion_data)
        return pd.DataFrame()  # 빈 데이터 반환

    date_counts = extract_dates(notion_data)
    
    if not date_counts:
        print("⚠️ 변환된 데이터가 없습니다!", date_counts)
        return pd.DataFrame(columns=["Date", "Count"])

    df = pd.DataFrame(list(date_counts.items()), columns=["Date", "Count"])
    
    print("📊 변환된 데이터프레임:", df)  # 데이터 출력

    df["Date"] = pd.to_datetime(df["Date"])

    # ✅ 데이터 반환 전에 타입 확인
    print("📌 `get_dataframe()`이 반환하는 타입:", type(df))

    return df.set_index("Date").sort_index()
