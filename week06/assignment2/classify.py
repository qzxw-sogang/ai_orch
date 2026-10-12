import json
import re
from mock_llm import mock_llm_call

SYSTEM = """당신은 고객 리뷰 분류기입니다.
반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트를 절대 포함하지 마세요.
{"category": "배송|품질|가격|환불|서비스|기타",
 "sentiment": "긍정|부정|중립",
 "score": 1~5 사이의 정수}"""

def classify_review(review_text):
    """리뷰 1건을 분류하여 딕셔너리로 반환. (data, fault_type) 튜플 반환. 실패 시 data는 None"""
    result = mock_llm_call(SYSTEM, f"리뷰: {review_text}")
    raw = result["text"].strip() # 결과 텍스트의 앞뒤 불필요한 공백과 줄바꿈을 제거
    fault_type = result["fault_type"]

    # 방어 1: 코드 펜스, 사족 제거, 텍스트에서 중괄호를 찾아 중괄호를 포함한 내용만 가져온다
    match = re.search(r"\{.*\}", raw, re.DOTALL) # 중괄호를 포함해 그 사이 모든 내용을 가져온다, re.DOTALL은 줄바꿈 무시하고 모든 문자열 매칭
    if match:
        raw = match.group() # 중괄호 포함한 전체

    # 방어 2: 파싱 실패는 언제든 일어날 수 있다 → 예외 처리 필수
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print(f"[경고] JSON 파싱 실패: {raw[:50]}...")
        return None, fault_type

    # 방어 3: 필드 존재와 값의 유효성 검증
    if data.get("category") not in ["배송", "품질", "가격", "환불", "서비스", "기타"]:
        return None, fault_type

    return data, fault_type
