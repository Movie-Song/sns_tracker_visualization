# test_notion.py
from notion_api import get_dataframe

# 데이터 가져오기
df = get_dataframe()

# 결과 출력
print("📌 get_dataframe() 반환 값:")
print(df)
print("📌 반환된 타입:", type(df))
print("📌 DataFrame 정보:")
print(df.info())
print("📌 DataFrame 미리보기:")
print(df.head())
