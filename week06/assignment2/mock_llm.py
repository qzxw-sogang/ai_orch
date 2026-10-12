# mock_llm.py — 6~12주차용 모의 LLM 모듈
import random

def mock_llm_call(system, user_message, temperature=0.2, max_tokens=500):
    """실제 API와 동일한 인터페이스를 갖는 모의 함수.
    13주차에 이 함수의 내부만 실제 Anthropic 호출로 교체한다."""
    reviews_keywords = {
        "배송": '{"category": "배송", "sentiment": "긍정", "score": 4}',
        "환불": '{"category": "환불", "sentiment": "부정", "score": 2}',
        "품질": '{"category": "품질", "sentiment": "긍정", "score": 5}',
        "보통": '{"category": "품질", "sentiment": "중립", "score": 5}',
        "파손": '{"category": "품질", "sentiment": "부정", "score": 1}',
    }

    random_rate = random.random() # 0부터 1 사이의 실수 생성
    random_int = random.randint(1, 3) # 1부터 3 사이의 정수 생성
    fault_type = None # 불량 유형
    text = '{"category": "기타", "sentiment": "중립", "score": 3}' # 디폴트 문자열
    stop_reason = 'end_turn'

    for keyword, content in reviews_keywords.items():
        if keyword in user_message:
            text = content
            break

    if random_rate < 0.2: # 20% 확률로 불량 답변 문자열 생성
        if random_int == 1: # 코드펜스 포함
            text = f'```json {text} ```'
            fault_type = "code_fence"
        elif random_int == 2: # 사족 포함
            text = f'물론입니다! 분석 결과는 다음과 같습니다. {text}'
            fault_type = "unnecessary"
        else: # 잘린 JSON
            text = text[:len(text)//2]
            fault_type = "truncated"
        
    return {"text": text, "stop_reason": stop_reason, "usage": {"input_tokens": 120, "output_tokens": 35}, "fault_type": fault_type}
