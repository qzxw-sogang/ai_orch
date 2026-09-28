스크립트 1
- 진단 보고  
    무엇이 - ValueError: invalid literal for int() with base 10: '5,200'  
    어디서 -  
        File "c:\Users\mingyu\Desktop\ai_orch\week04\buggy_1.py", line 19, in calc_total  
        price = int(row["price"])  
    왜 - 5,200에 쉼표가 들어가 있어 int()에서 정수로 바꿔주지 못한 것으로 추정된다.

- 프롬프트  
    ① 맥락 무엇을 하려는 코드인가 (한두 문장)  
    판매 데이터를 읽어와 매출을 집계하는 스크립트인데  

    ② 코드 관련된 최소 범위의 코드 (전체 붙여넣기 금지)  
    price = int(row["price"])에서 오류가 발생해  

    ③ Traceback 에러 로그 전문 (요약하지 말고 그대로)  

    Traceback (most recent call last):
    File "c:\Users\mingyu\Desktop\ai_orch\week04\buggy_1.py", line 25, in <module>
        total = calc_total("./Week4/dirty_sales.csv")
    File "c:\Users\mingyu\Desktop\ai_orch\week04\buggy_1.py", line 19, in calc_total
        price = int(row["price"])
    ValueError: invalid literal for int() with base 10: '5,200'

    ④ 내가 확인한 것 print/디버거로 파악한 변수 상태와 나의 가설  
    내 생각에는 5,200에 쉼표가 들어가 있어 int()에서 정수로 바꿔주지 못한 것으로 추정돼  

    ⑤ 요청 원하는 답의 형태를 지정  
    원인이 뭔지 설명해주고 price 데이터에 int변환 할때 문제가 될수 있는 행이 있을지 찾는 방법을 제시해줘

- 답변  
    int()에 문자열을 넘기면 공백, 부호(+/-), 숫자로만 된 문자열만 정수로 바꿉니다. 숫자 사이의 밑줄(1_000)도 예외적으로 허용됩니다. 쉼표는 허용되지 않기 때문에 '5,200'은 숫자가 아닌 문자열로 보고 ValueError가 납니다.

    int("5200")    # 5200
    int(" 5200 ")  # 5200  (앞뒤 공백은 괜찮음)
    int("5,200")   # ValueError  ← 지금 상황

    CSV는 모든 값을 문자열로 읽습니다. 그래서 원본 데이터에 사람이 보기 좋게 넣은 천 단위 쉼표가 그대로 int()에 들어간 것입니다. 파일 이름이 dirty_sales.csv이니 쉼표 말고도 다음 값들이 섞여 있을 가능성이 큽니다.

    값 예시	int() 결과  
    '' (빈 칸)	ValueError  
    'N/A', '-', '없음'	ValueError  
    '5200.0' (소수점)	ValueError (int(float(...))로는 가능)  
    '5200원', '₩5,200'	ValueError  
    None (열 개수가 모자란 행)	TypeError  
    '-5200'	변환은 되지만 매출로는 이상한 값

    문제 행 찾는 방법  
    변환에 실패한 행을 전부 모아서 출력하기

    지금은 첫 오류에서 멈추기 때문에 문제 행을 하나밖에 볼 수 없습니다. try/except로 실패를 기록하면서 끝까지 읽으면 전체 목록을 얻을 수 있습니다.

- 채택, 검증 결과  
    try, except 구문을 통해 확인한 결과

        try:
            price = int(row["price"]) 
        except:
            rint(row["price"])

        결과
        5,200
        4200원
        3,500
        12,000
        18,000

        5500원
        4,200
        4,500
        4,500

        5,000
    
    다수의 결측치와 쉼표, "원" 표시가 붙은 데이터들이 존재하는 것을 확인함

- 수정한 코드의 설명  
    작성하신 코드는 데이터의 예외 상황(결측치, 지분 지저분한 문자열)을 안전하게 처리하여 정상적인 숫자만 집계에 포함하도록 정제하는 로직입니다.  
    두 부분으로 나누어 설명해 드립니다.
    1. 결측치(빈값) 패스 처리
    동작 방식: price 데이터가 빈 문자열('')인지 확인합니다.처리 결과: 데이터가 비어 있다면 아래 계산 과정을 거치지 않고 continue를 통해 다음 행(데이터)으로 바로 넘어갑니다.
    효과: 빈 값을 int()로 변환하려 할 때 발생하는 ValueError를 방지하고, 합계 계산에서 제외합니다.
    2. 불필요한 문자 제거 및 정수 변환
    동작 방식 (체이닝 방식):  
    .strip(): 문자열 앞뒤에 혹시 붙어있을 공백(스페이스, 탭 등)을 제거합니다. (예: ' 5,200원 ' -> '5,200원')  
    .replace(",", ""): 쉼표(,)를 없앱니다. (예: '5,200원' -> '5200원')  
    .replace("원", ""): 한글 '원'을 없앱니다. (예: '5200원' -> '5200')  
    int(...): 최종적으로 남은 순수 숫자 문자열 '5200'을 정수 5200으로 변환합니다.효과: 다양한 양식(5,200, 5200원, 5,200원 등)으로 들어온 금액 데이터를 깔끔하게 숫자로 통일하여 에러 없이 집계할 수 있게 만듭니다.

- 검증 의견
    의도한 바를 정확하게 파악했고 동작 원리 역시 정확했다.

스크립트 2
- 진단 보고  
    무엇이 - KeyError: '단가'  
    어디서 -  
    File "c:\Users\mingyu\Desktop\ai_orch\week04\buggy_2.py", line 20, in summarize
    df["매출액"] = df["단가"] * df["수량"]    
    왜 - csv 파일의 열에 "단가"라는 항목이 존재하지 않는 것을 확인했다.

- AI 미사용

스크립트 3
- 진단 보고  
    무엇이 - AttributeError: 'NoneType' object has no attribute 'groupby'  
    어디서 -  
    File "c:\Users\mingyu\Desktop\ai_orch\week04\buggy_3.py", line 28, in main
    result = df.groupby("category")["revenue"].sum()   
    왜 - load_and_clean 함수 마지막에서 새로운 df가 반환되지 않아 main에 선언된 df 변수가 NoneType 객체로 인식된 것으로 추정된다.

- AI 미사용

스크립트 4
- 진단 보고  
    어떻게 알았는지 -  
        <class 'pandas.DataFrame'>
        RangeIndex: 500 entries, 0 to 499
        Data columns (total 6 columns):  
        #   Column    Non-Null Count  Dtype  
        ---  ------    --------------  -----  
        0   date      500 non-null    str    
        1   product   500 non-null    str    
        2   category  490 non-null    str    
        3   price     498 non-null    float64
        4   quantity  500 non-null    int64  
        5   stock     485 non-null    float64
        dtypes: float64(2), int64(1), str(3)
        memory usage: 23.6 KB
        None
                    price      quantity       stock
        count  4.980000e+02  5.000000e+02  485.000000  
        mean   2.834237e+04  2.010569e+04  249.995876  
        std    4.477810e+05  4.472088e+05  141.211450  
        min   -4.500000e+03  1.000000e+00    1.000000  
        25%    3.800000e+03  5.375000e+01  128.000000  
        50%    5.000000e+03  1.120000e+02  250.000000  
        75%    1.200000e+04  1.610000e+02  363.000000  
        max    9.999999e+06  9.999999e+06  500.000000  
    
    무엇이 틀렸는지 - price 열에 결측치가 2개 있고 최솟값에 음수, 최댓값에 9999999가 들어있다. quantity 열에도 최댓값에 9999999가 들어있다.

- 프롬프트  
    ① 맥락 무엇을 하려는 코드인가 (한두 문장)  
    총 매출액 집계하는 스크립트

    ② 코드 관련된 최소 범위의 코드 (전체 붙여넣기 금지)   
        df["price"] = (df["price"].astype(str)
                                .str.replace(",", "")
                                .str.replace("원", "")
                                .str.strip())
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    ③ Traceback 에러 로그 전문 (요약하지 말고 그대로)  
    없음

    ④ 내가 확인한 것 print/디버거로 파악한 변수 상태와 나의 가설  
    <class 'pandas.DataFrame'>
        RangeIndex: 500 entries, 0 to 499
        Data columns (total 6 columns):  
        #   Column    Non-Null Count  Dtype  
        ---  ------    --------------  -----  
        0   date      500 non-null    str    
        1   product   500 non-null    str    
        2   category  490 non-null    str    
        3   price     498 non-null    float64
        4   quantity  500 non-null    int64  
        5   stock     485 non-null    float64
        dtypes: float64(2), int64(1), str(3)
        memory usage: 23.6 KB
        None
                    price      quantity       stock
        count  4.980000e+02  5.000000e+02  485.000000  
        mean   2.834237e+04  2.010569e+04  249.995876  
        std    4.477810e+05  4.472088e+05  141.211450  
        min   -4.500000e+03  1.000000e+00    1.000000  
        25%    3.800000e+03  5.375000e+01  128.000000  
        50%    5.000000e+03  1.120000e+02  250.000000  
        75%    1.200000e+04  1.610000e+02  363.000000  
        max    9.999999e+06  9.999999e+06  500.000000  
    price 열에 결측치가 2개 있고 최솟값에 음수, 최댓값에 9999999가 들어있어, quantity 열에도 최댓값에 9999999가 들어있는 상황이야

    ⑤ 요청 원하는 답의 형태를 지정  
    전체적인 결측치, 이상치를 찾아내서 이 값들을 제외하고 총매출을 집계하려면 어떤 방식으로 처리하는게 좋을지 처리 방안을 여러개 제시해줘

- 답변  
    지금 데이터에서 읽히는 것
    9,999,999는 이상치라기보다 "값 없음"을 표시한 코드일 가능성이 큽니다. quantity는 25~75% 구간이 54~161인데 최댓값만 9,999,999입니다. 평균이 20,105로 크게 튄 것도 이 값 하나 때문으로 보입니다(9,999,999 ÷ 500 ≈ 20,000). 이런 값은 통계 기법으로 찾기 전에 규칙으로 먼저 걸러야 합니다.  

    음수 가격(-4,500)은 오류일 수도, 환불·반품일 수도 있습니다. 뺄지 말지는 코드 문제가 아니라 "총매출"을 어떻게 정의하느냐의 문제입니다. 판매액만 더한 총매출이면 제외하고, 환불을 차감한 순매출이면 포함합니다.  

    category(결측 10개)와 stock(결측 15개)은 매출 계산에 쓰이지 않습니다. df.dropna()를 그냥 쓰면 매출과 상관없는 행까지 최대 25개가 사라집니다. 결측치는 price와 quantity 기준으로만 판단해야 합니다.  
    
    price 결측 2개가 원래 빈 칸인지, 변환에 실패한 값인지 모릅니다. errors="coerce"는 'N/A'나 '5200.0.0' 같은 값도 조용히 NaN으로 바꿉니다. 어떤 경우인지 한 번 확인해 두는 것이 좋습니다.  
    
    먼저 할 일: 변환 실패 값과 특수 코드 확인
        '''

        raw = df["price"].copy()  
        df["price"] = pd.to_numeric(
        raw.astype(str).str.replace(",", "").str.replace("원", "").str.strip(),
        errors="coerce")

        # 원래 값이 있었는데 NaN이 된 것 = 변환 실패
        print("변환 실패:", raw[df["price"].isna() & raw.notna()].unique())

        # 9999999, -1, 0 같은 특수 코드가 더 있는지 확인
        for col in ["price", "quantity"]:
            print(col, df[col].value_counts().sort_index().tail(5), sep="\n")
            print(col, "<= 0:", (df[col] <= 0).sum())
        '''  
      
    처리방안 1. 업무 규칙 기반 필터

    "가격은 0보다 크다", "수량은 1 이상이다", "9,999,999는 무효값이다"처럼 설명할 수 있는 규칙으로 거릅니다. 어떤 행이 왜 빠졌는지 명확합니다. 행을 바로 지우지 말고 플래그 열을 만들어 두는 것이 핵심입니다. 그래야 나중에 사유별 개수를 보고할 수 있습니다.  
    
    처리방안 2. 상품별 기준 가격과 비교

    같은 상품은 가격이 거의 일정하다는 점을 이용합니다. 각 상품의 중앙값 가격과 비교해 몇 배 이상 벗어나면 이상치로 봅니다. 중앙값은 9,999,999 같은 극단값에 흔들리지 않기 때문에 이 데이터에 잘 맞습니다.
      
    방안 3. IQR (사분위 범위) 방식

    Q1 − 1.5×IQR 아래나 Q3 + 1.5×IQR 위에 있는 값을 이상치로 봅니다. 사분위수는 극단값의 영향을 덜 받기 때문에 평균과 표준편차를 쓰는 Z-score보다 이 데이터에 적합합니다. 지금 price의 표준편차(447,781)는 9,999,999 때문에 크게 부풀어 있어서, Z-score로는 다른 이상치가 오히려 묻힐 수 있습니다.

    방안 4. 제외하지 않고 보정  

    price 결측치를 같은 상품의 중앙값 가격으로 채우는 방법도 있습니다.

- 채택, 검증 결과  
    결측치, 이상치 확인 결과  

        변환 실패: <StringArray>
        []
        Length: 0, dtype: str
        price
        price
        12000.0      42
        15000.0      41
        18000.0      42
        21000.0      39
        9999999.0     1
        Name: count, dtype: int64
        price <= 0: 1
        quantity
        quantity
        197        2
        198        1
        199        3
        200        4
        9999999    1
        Name: count, dtype: int64
        quantity <= 0: 0

    변환 이상은 없으니 가격 결측치는 원래 변환 중 오류는 아님, 가격에 음수 데이터 1개 존재, 가격, 수량에 각각 9999999가 1개씩 존재하는 것을 확인  

    결측치와 이상치가 단순하게 나눠져 있으므로 방안1을 적용해 총매출을 계산한다.  
    음수 데이터와 9999999 데이터는 그 수가 많지 않고 총매출에 큰 영향을 주므로 제외하여 계산한다.  
    이 방식을 적용해 출력한 결과와 AI를 통해 계산한 결과를 비교해본다.
    수정된 코드의 결과와 AI의 결과가 동일하다.

        항목	    수정 전 (원래 코드)	 수정 후 (정상 데이터만)
        집계 행 수	500행 	            495행
        총매출액	151,198,388,824원	438,939,400원
        평균 단가	28,342원	        8,291원 (8,290.91)

스크립트 5
- 진단 보고  
    무엇이 - IndexError: list index out of range  
    어디서 -  
        File "c:\Users\mingyu\Desktop\ai_orch\week04\buggy_5.py", line 36, in <module>
        jumps = find_big_jumps(prices)
        File "c:\Users\mingyu\Desktop\ai_orch\week04\buggy_5.py", line 29, in find_big_jumps
        diff = prices[i + 1] - prices[i]  
    왜 - i가 len(prices)-1(이 경우, 499)이 되면 prices[i + 1]에서 i+1(500)이 인덱스를 벗어나게 되는 것으로 추정된다.

- AI 미사용