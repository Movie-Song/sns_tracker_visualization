def extract_dates(data):
    """ 날짜별 카운트 집계 + 데이터 출력 추가 """
    date_counts = defaultdict(int)

    for item in data.get("results", []):
        properties = item.get("properties", {})

        # ✅ Date 필드 확인
        date_property = properties.get("Date", {}).get("date", {})
        print("📅 가져온 날짜 데이터:", date_property)  # 디버깅 출력

        if "start" in date_property:
            date = date_property["start"]
            date_counts[date] += 1

    print("📊 최종 날짜별 데이터 카운트:", date_counts)  # 디버깅 출력
    return date_counts
