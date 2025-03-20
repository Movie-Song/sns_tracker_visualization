import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from collections import defaultdict

# 환경 변수에서 노션 API 키 및 데이터베이스 ID 가져오기
NOTION_API_KEY = os.getenv("NOTION_API_KEY")  # GitHub Secrets에서 불러옴
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")  # GitHub Secrets에서 불러옴

# 노션 API 요청을 위한 헤더 설정
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_notion_data():
    """
    노션 데이터베이스에서 지난 1년치 데이터를 가져온다.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    # 지난 1년간 데이터 필터링
    one_year_ago = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    
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

    if "results" not in data:
        print("❌ 노션 API 응답 오류:", data)
        return []

    return data["results"]

def process_notion_data():
    """
    노션에서 가져온 데이터를 가공하여 날짜별 개수 집계.
    """
    notion_data = get_notion_data()
    date_count = defaultdict(int)

    for page in notion_data:
        properties = page.get("properties", {})
        date_property = properties.get("Date", {}).get("date", {})

        if date_property and "start" in date_property:
            date_str = date_property["start"][:10]  # YYYY-MM-DD 형식 추출
            date_count[date_str] += 1

    return date_count

def get_dataframe():
    """
    날짜별 개수 데이터를 pandas DataFrame으로 변환하여 반환.
    """
    date_count = process_notion_data()

    if not date_count:
        print("⚠️ 데이터 없음! 노션 API 응답을 확인하세요.")
        return pd.DataFrame()  # 빈 데이터프레임 반환

    df = pd.DataFrame(list(date_count.items()), columns=["Date", "Count"])
    df["Date"] = pd.to_datetime(df["Date"])  # 날짜 형식 변환
    df = df.set_index("Date").sort_index()  # 날짜를 인덱스로 설정하고 정렬

    print("📊 변환된 데이터프레임:")
    print(df.head())  # 상위 5개 데이터 미리보기

    return df
