# 리뷰 데이터를 classify로 보내고 classify에서 불량 응답 개수, 처리 실패 횟수 등의 정보를 정리해 보여주는 역할
import csv
from classify import classify_review

total_count = 0 # 전체 실행 횟수
failed = 0 # 실패 횟수
fault_list = ["code_fence", "unnecessary", "truncated"]
fault_count = {k: 0 for k in fault_list} # 유형별 불량 응답 횟수
recovered = {k: 0 for k in fault_list} # 유형별 복구 성공 횟수

with open("reviews_sample.csv", "r", encoding="utf-8-sig", newline="") as f:
    reviews = csv.DictReader(f)

    for r in reviews:
        result, fault_type = classify_review(r["review_text"]) 
        total_count += 1
        if fault_type is not None:
            fault_count[fault_type] += 1
            if result is not None: # 불량이었지만 방어 코드가 살려낸 경우
                recovered[fault_type] += 1

        if result is None: # 실패 횟수
            failed += 1
            continue

total_faults = sum(fault_count.values())
total_recovered = sum(recovered.values())

print("\n" + "=" * 44)
print(f"처리 {total_count}건 / 실패 {failed}건")
print("=" * 44)
print(f"불량 응답 {total_faults}건 (전체의 {total_faults / total_count:.1%})")
for label in fault_list:
    print(f"{label} {fault_count[label]}건 중 {recovered[label]}건 복구")
print(f"→ 복구 {total_recovered}건, 실패 {failed}건")
print(f"  (실패 {failed}건 < 불량 {total_faults}건인 이유: "
        f"코드펜스형 {recovered['code_fence']}건, 사족형 {recovered['unnecessary']}건을 방어 1이 복구했기 때문)")
print("-" * 44)