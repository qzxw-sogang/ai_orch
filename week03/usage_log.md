1. 데이터 로드 후 shape과 info() 확인 결과
    ```
    RAW_DATA.csv shape, info
    (500, 5)
    <class 'pandas.DataFrame'>
    RangeIndex: 500 entries, 0 to 499
    Data columns (total 5 columns):
    #   Column  Non-Null Count  Dtype
    ---  ------  --------------  -----
    0   주문일자    500 non-null    str  
    1   상품명     500 non-null    str  
    2   카테고리    500 non-null    str  
    3   단가      500 non-null    str  
    4   수량      500 non-null    int64
    dtypes: int64(1), str(4)
    memory usage: 19.7 KB
    None
    ```

2. AI 사용 기록
- 질문 1
    + report = df.groupby(["month", "category"])["sales"].agg(
    총매출="sum", 평균매출="mean", 거래건수="count")
    agg 함수에서 "sum", "mean", "count"는 무슨 역할이야?

- 답변 1
    + agg()에 "sum", "mean", "count"를 문자열로 넘기면, pandas는 이 이름을 보고 GroupBy 객체의 자체 메서드를 대신 실행해요.
    "sum"   → GroupBy.sum()    # 그룹별 합계
    "mean"  → GroupBy.mean()   # 그룹별 평균
    "count" → GroupBy.count()  # 그룹별 값의 개수 (NaN 제외)
    그래서 사실상 아래 코드와 같은 결과가 나옵니다.
    g = df.groupby(["month", "category"])["sales"]
    g.sum(), g.mean(), g.count()
    이 문법은 Named Aggregation(이름 붙인 집계)이라고 해요. 결과컬럼이름 = "집계함수" 형태로 씁니다. 결과 표의 열 이름이 sum, mean, count 대신 총매출, 평균매출, 거래건수로 나와요.

- 질문 2
    + print(df.head)나 print(report)처럼 판다스에서 생성한 객체를 터미널에서 출력해보면 맨 위 줄의 범주하고 아래 데이터들 사이에 정렬이 안돼서 불편한데 해결할 수 있는 방법이 있어?

- 답변 2
    + 터미널에서 한글은 영문보다 2배 넓은 칸(전각 문자)을 차지해요. 그런데 pandas는 기본적으로 한글도 1칸으로 계산해서 열 간격을 맞추기 때문에 줄이 어긋나요.  

        해결: 동아시아 문자 폭 옵션 켜기
        코드 위쪽(import 바로 아래)에 추가하세요.
        import pandas as pd
        pd.set_option("display.unicode.east_asian_width", True)
        pd.set_option("display.unicode.ambiguous_as_wide", True)  # 일부 특수문자까지 보정  

        함께 쓰면 좋은 옵션
        열이 많아서 ...으로 생략되거나 줄이 넘어갈 때 쓰면 좋아요.  
        pd.set_option("display.max_columns", None)  # 모든 열 표시
        pd.set_option("display.width", 200)         # 한 줄 출력 폭 늘리기

- 질문 3
    + pd.set_option("display.unicode.east_asian_width", True) pd.set_option("display.unicode.ambiguous_as_wide", True) 이 코드들이 다른 환경에서 문제를 일으키진 않겠지?

- 답변 3
    + 문제가 없는 이유
    출력 모양에만 영향을 줘요. print(df)나 df.to_string()처럼 텍스트로 표시할 때의 칸 계산만 바뀌어요. 데이터 값, 계산 결과, to_csv()나 to_excel()로 저장한 파일에는 전혀 영향이 없어요.
    현재 실행 중인 파이썬 프로세스에만 적용돼요. 다른 스크립트, 다른 사람의 컴퓨터, 시스템 설정은 바뀌지 않아요.
    Jupyter Notebook에서 표가 HTML로 렌더링될 때는 이 옵션이 사용되지 않아서 차이가 없어요.

        주의할 만한 점
        ambiguous_as_wide는 환경에 따라 오히려 어긋날 수 있어요. 이 옵션은 ①, →, ·, °, × 같은 "애매한 폭" 문자를 2칸으로 계산하게 해요. 그런데 영문 윈도우나 맥, 리눅스처럼 한국어가 아닌 환경의 터미널은 이런 문자를 보통 1칸으로 그려요. 그래서 이런 기호가 데이터에 있으면 정렬이 틀어질 수 있어요.
        → 한글 정렬만 필요하면 east_asian_width 하나만 써도 충분해요. ambiguous_as_wide는 특수기호가 어긋날 때만 추가하는 걸 권장해요.
        아주 큰 데이터를 출력할 때 약간 느려질 수 있어요. 문자마다 폭을 계산하기 때문인데, head() 정도의 출력에서는 체감되지 않아요.

- 답변 3 채택 내용, 결과
    + pd.set_option("display.unicode.east_asian_width", True)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

        pd.set_option("display.unicode.ambiguous_as_wide", True)는 예외를 만들지 않기 위해 채택하지 않음

    +          주문일자    상품명  카테고리  단가  수량
            0  2026-01-01  크루아상  베이커리  4500     1
            1  2026-01-01      스콘    디저트  4000     3
            2  2026-01-01    크로플    디저트  6000     2
            3  2026-01-01  크루아상  베이커리  4500     3
            4  2026-01-01  샌드위치  베이커리  7000     1
        정상적으로 열에 맞게 출력된다.

- 질문 4
    + df.groupby("카테고리")["매출액"].sum().sort_values("매출액", ascending= False)
    groupby에서 나온 결과를 sort_values()를 통해 내림차순으로 정렬하려는데 뭐가 문제일까?

- 답변 4
    + 문제는 결과가 DataFrame이 아니라 Series라는 점이에요.
        원인
        df.groupby("카테고리")["매출액"].sum()

        ["매출액"]처럼 대괄호 하나로 열 하나를 고르면, 집계 결과는 Series가 돼요. 인덱스는 카테고리, 값은 매출액 합계예요. Series는 열이 하나뿐이라 sort_values()에 정렬할 열 이름을 넣을 필요가 없고, 넣으면 안 돼요.

        Series의 sort_values()에서 첫 번째 인자는 열 이름이 아니라 axis예요. 그래서 "매출액"이 축 이름으로 해석되고, 이런 오류가 나요.
        ValueError: No axis named 매출액 for object type Series

        해결 1: 열 이름 빼기
        df.groupby("카테고리")["매출액"].sum().sort_values(ascending=False)

        해결 2: DataFrame으로 받아서 열 이름으로 정렬
        대괄호를 두 겹으로 쓰면 결과가 DataFrame이 되므로, 열 이름을 지정해서 정렬할 수 있어요.
        df.groupby("카테고리")[["매출액"]].sum().sort_values("매출액", ascending=False)

- 답변 4 채택 내용, 결과
    + 열 이름 빼기 df.groupby("카테고리")["매출액"].sum().sort_values(ascending=False)
    + 
            카테고리                                                                                                                    
            음료         1915000
            디저트       1340000     
            베이커리     682500
            Name: 매출액, dtype: Int64
        정상적으로 내림차순으로 출력된다.


- 질문 5
    + by_cat.reset_index().to_excel(writer, sheet_name="카테고리별", index=False)에서 reset_index() 역할이 뭐야?

- 답변 5
    + reset_index()는 인덱스로 들어가 있던 값을 일반 열로 꺼내고, 인덱스는 0, 1, 2… 번호로 새로 매기는 역할을 해요.

        변환 전 (by_cat)
        groupby("카테고리") 결과라서 카테고리가 인덱스예요.
        카테고리       ← 인덱스 이름
        음료    150000
        식품    120000

        변환 후 (by_cat.reset_index())
        카테고리가 일반 열로 내려오고, 인덱스는 새 번호가 돼요.
        카테고리   매출액
        0   음료   150000
        1   식품   120000

        이 코드에서 필요한 이유
        뒤에 index=False가 붙어 있죠. 이 옵션은 인덱스를 엑셀에 저장하지 말라는 뜻이에요.
        reset_index()가 없으면: 인덱스인 카테고리가 버려져서 매출액만 저장돼요.
        reset_index()가 있으면: 카테고리는 이미 일반 열이 되었으니 그대로 저장되고, 버려지는 건 의미 없는 번호(0, 1, 2…)뿐이에요.
        즉, 두 옵션이 짝을 이뤄서 "카테고리 | 매출액" 형태의 깔끔한 표를 엑셀 시트에 저장하는 거예요.