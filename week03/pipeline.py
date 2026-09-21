import pandas as pd

df = pd.read_csv("RAW_DATA.csv", encoding="cp949")
print("RAW_DATA.csv shape, info")
print(df.shape) 
print(df.info())
