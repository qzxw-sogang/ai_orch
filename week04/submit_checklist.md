1. buggy_1 ~ buggy_5 진단 보고 각 3~5줄 (3단계 루틴 형식)  
    usage_lod.md 파일에 파일별로 작성함

2. 수정 부분 # FIXED 주석 표기  
    buggy_1 -> 19, 21행  
    buggy_2 -> 20행  
    buggy_3 -> 24행  
    buggy_4 -> 26, 27, 30, 32, 33행  
    buggy_5 -> 28행  

3. 스크립트당 fix: 커밋 최소 1개  
    커밋 히스토리 확인  

4. 수정 후 정상 실행 증빙 + 회귀 확인 1가지  
    buggy_4와 관련해 buggy4_before_after_comparison.png, buggy4_cleaned_data_summary.png, buggy4_successful_run_result.png 는 정상 실행 출력 결과를 보여주는 이미지 파일  
    usage_log의 buggy_4 채택, 검증결과 항목에 추가 설명  
    기존에는 위 사항만으로도 충분히 회귀 없음이 판단된다고 생각해 추가적인 자료를 제출하지 않았으나 추가적인 실험을 통한 데이터를 추가 제출함  
    regression_before_result.png, regression_after_result.png, test_csv.png  
    테스트 csv 파일(test_csv.png에 나온 내용)을 생성해서 수정 전(오류 존재) 코드로 테스트 csv 파일을 실행했을 때의 결과와 수정 후 코드로 실행했을 때의 결과가 같음을 보이고 손으로 계산한 값도 같음을 나타냄  

5. usage_log.md: 템플릿 5요소 프롬프트 최소 2건  
    buggy_1, 4에서 5요소 프롬프트 적용, 이외는 AI 미사용

6. AI에게 코드 설명 요구 + 본인 검증 의견 최소 1건  
    usage_log의 buggy_1 항목에 수정한 코드의 설명, 본인 의견 작성함

