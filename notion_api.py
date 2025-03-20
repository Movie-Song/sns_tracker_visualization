import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv

# .env 파일에 저장된 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수에서 Notion API 키와 데이터베이스 ID를 읽어옵니다.
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

if not NOTION_API_KEY or not DATABASE_ID:
    print("Error: NOTION_API_KEY와 DATABASE_ID 환경 변수가 올바르게 설정되지 않았습니다.")

# Notion API 호출을 위한 헤더를 설정합니다.
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_notion_data():
    """
    Notion API에서 지난 1년치 데이터를 가져옵니다.
    데이터베이스 ID는 환경 변수 DATABASE_ID에 저장되어 있어야 합니다.
    """
    one_year_ago = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Date",
            "date": {
                "on_or_after": one_year_ago
            }
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    data = response.json()
    if "error" in data:
        print("Error from Notion API:", data)
        return []
    return data.get("results", [])

def process_notion_data():
    """
    Notion에서 가져온 데이터를 날짜별로 집계하여 딕셔너리 형태로 반환합니다.
    (날짜는 'YYYY-MM-DD' 형식)
    """
    pages = get_notion_data()
    date_counts = defaultdict(int)
    for page in pages:
        properties = page.get("properties", {})
        # "Date" 속성이 올바르게 설정되어 있어야 합니다.
        date_field = properties.get("Date", {}).get("date", {})
        if date_field and "start" in date_field:
            # 날짜 문자열에서 앞의 10자리(YYYY-MM-DD)만 추출합니다.
            date_str = date_field["start"][:10]
            date_counts[date_str] += 1
    return date_counts

def get_dataframe():
    """
    날짜별 집계 데이터를 Pandas DataFrame으로 변환하여 반환합니다.
    반환되는 DataFrame은 인덱스가 날짜(datetime)로 설정되어 있습니다.
    """
    counts = process_notion_data()
    if not counts:
        print("⚠️ 변환된 데이터가 없습니다. Notion API 응답을 확인하세요.")
        return pd.DataFrame()
    df = pd.DataFrame(list(counts.items()), columns=["Date", "Count"])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date").sort_index()
    print("📊 변환된 데이터프레임 (상위 5개):")
    print(df.head())
    return df
