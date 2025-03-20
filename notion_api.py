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
    """ 최근 1년 데이터 가져오기 + API 응답 출력 """
    one_year_ago = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    payload = {
        "filter": {
            "property": "Date",  # 필드명 확인 필요!
            "date": {
                "after": one_year_ago  # 1년 전 이후 데이터만 가져오기
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # ✅ API 응답 출력 (디버깅용)
    print("🔍 API 응답 데이터:", data)

    return data

def extract_dates(data):
    """ 날짜별 카운트 집계 """
    date_counts = defaultdict(int)
    for item in data.get("results", []):
        properties = item.get("properties", {})

        # ✅ 노션의 'Date' 필드명이 맞는지 확인 필요!
        date_property = properties.get("Date", {}).get("date", {})
        if "start" in date_property:
            date = date_property["start"]
            date_counts[date] += 1
    return date_counts

def get_dataframe():
    """ 데이터프레임 변환 """
    notion_data = get_notion_data()

    # ✅ API 응답이 정상인지 확인
    if "results" not in notion_data:
        print("⚠️ API에서 데이터를 가져오지 못함!", notion_data)
        return pd.DataFrame()  # 빈 데이터 반환

    date_counts = extract_dates(notion_data)
    df = pd.DataFrame(list(date_counts.items()), columns=["Date", "Count"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date").sort_index()
