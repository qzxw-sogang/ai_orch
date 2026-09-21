import pandas as pd

df = pd.read_csv("RAW_DATA.csv", encoding="cp949")
# print("RAW_DATA.csv shape, info")
# print(df.shape) 
# print(df.info())

df["단가"] = (pd.to_numeric(df["단가"].astype(str).str.replace(",", "", regex=False), errors="coerce").astype("Int64"))
# print(df.head)

df["매출액"] = df["단가"] * df["수량"]
# print(df.head)