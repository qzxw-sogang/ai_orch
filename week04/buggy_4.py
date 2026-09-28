# -*- coding: utf-8 -*-
"""
buggy_4.py  ―  총 매출액 집계 (에러 없이 '조용히' 틀리는 스크립트)

이 스크립트는 에러 없이 잘 돌아가고, 그럴듯한 숫자를 출력한다.
하지만 그 숫자는 '틀렸다'.

[과제] 이 스크립트는 예외를 던지지 않는다. 대신
       (1) info()/describe()로 데이터 상태를 먼저 세어 보고
       (2) '무엇이 틀렸는지 어떻게 알아챘는지'를 서술한 뒤
       (3) 결측 규모를 보고하고 처리 방법을 선택·적용하여
           올바른 총매출을 산출하라.
       (힌트: 가격 결측은 몇 건인가? 음수 가격과 9999999 같은 값은 정상인가?)
"""
import pandas as pd

def main():
    df = pd.read_csv("dirty_sales.csv", encoding="utf-8")

    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    valid = (df["price"] > 0) & (df["price"] != 9999999) & (df["quantity"] != 9999999) # FIXED: 유효하지 않은 데이터가 있는 행 자체를 제외
    df_valid = df[valid] # FIXED: 정상적인 데이터만 있는 데이터프레임 

    # 매출액 = 단가 x 수량
    df_valid["revenue"] = df_valid["price"] * df_valid["quantity"] # FIXED: 변수명 변경 

    total = df_valid["revenue"].sum() # FIXED: 변수명 변경
    avg_price = df_valid["price"].mean() # FIXED: 변수명 변경
    
    # print(df_valid.info())
    # print(df_valid.describe())

    print(f"총 매출액: {total:,.0f}원")
    print(f"평균 단가: {avg_price:,.0f}원")


    # raw = df["price"].copy()  
    # df["price"] = pd.to_numeric(
    #     raw.astype(str).str.replace(",", "").str.replace("원", "").str.strip(),
    #     errors="coerce")

    # # 원래 값이 있었는데 NaN이 된 것 = 변환 실패
    # print("변환 실패:", raw[df["price"].isna() & raw.notna()].unique())

    # # 9999999, -1, 0 같은 특수 코드가 더 있는지 확인
    # for col in ["price", "quantity"]:
    #     print(col, df[col].value_counts().sort_index().tail(5), sep="\n")
    #     print(col, "<= 0:", (df[col] <= 0).sum())

if __name__ == "__main__":
    main()
