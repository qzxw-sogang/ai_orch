import pandas as pd
pd.set_option("display.unicode.east_asian_width", True)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv("RAW_DATA.csv", encoding = "cp949")
# print("RAW_DATA.csv shape, info")
# print(df.shape) 
# print(df.info())

df["단가"] = (pd.to_numeric(df["단가"].astype(str).str.replace(",", "", regex=False), errors = "coerce").astype("Int64"))
# print(df.head())

df["매출액"] = df["단가"] * df["수량"]
# print(df.head())

df["주문일자"] = pd.to_datetime(df["주문일자"])
df["월"] = df["주문일자"].dt.month
# print(df.head())

report = df.groupby(["월", "카테고리"])["매출액"].agg(
총매출 = "sum", 평균매출 = "mean", 거래건수 = "count")
report = report.reset_index() # 그룹 키를 일반 열로 되돌리기
# print(report)

by_cat = df.groupby("카테고리")["매출액"].sum().sort_values(ascending = False)
# print(by_cat.head())

with pd.ExcelWriter("Monthly_Report.xlsx", engine = "openpyxl") as writer:
    report.to_excel(writer, sheet_name = "월별카테고리요약", index = False)
    by_cat.reset_index().to_excel(writer, sheet_name = "카테고리별합계", index = False)

assert df["매출액"].sum() == report["총매출"].sum(), "원본 매출액 총합과 집계표 총매출 합이 일치하지 않습니다"