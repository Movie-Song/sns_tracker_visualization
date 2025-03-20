import os
import requests
import pandas as pd
from dotenv import load_dotenv
from collections import defaultdict

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
    """ 노션 API에서 데이터 가져오기 """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
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

