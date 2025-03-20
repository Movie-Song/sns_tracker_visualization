from notion_api import get_dataframe

df = get_dataframe()

print("📌 get_dataframe() 반환 값:")
print(df)
print("📌 반환된 타입:", type(df))
print("📌 DataFrame 정보:")
print(df.info())
print("📌 DataFrame 미리보기:")
print(df.head())
