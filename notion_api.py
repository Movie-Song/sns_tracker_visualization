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
    """ 최근 1년 데이터만 가져오기 """
    # 1년 전 날짜 계산
    one_year_ago = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    # ✅ 노션 API 필터 추가 (최근 1년 데이터만 가져오기)
    payload = {
        "filter": {
            "property": "Date",
            "date": {
                "after": one_year_ago  # 1년 전 이후 데이터만 가져오기
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def extract_dates(data):
    """ 날짜별 카운트 집계 """
    date_counts = defaultdict(int)
    for item in data.get("results", []):
        properties = item.get("properties", {})
        date_property = properties.get("Date", {}).get("date", {})
        if "start" in date_property:
            date = date_property["start"]
            date_counts[date] += 1
    return date_counts

def get_dataframe():
    """ 데이터프레임 변환 """
    notion_data = get_notion_data()
    date_counts = extract_dates(notion_data)
    df = pd.DataFrame(list(date_counts.items()), columns=["Date", "Count"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date").sort_index()
