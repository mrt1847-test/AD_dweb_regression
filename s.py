import json

# JSON 로드
with open("json/test_srp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 상품번호만 뽑기
product_ids = []
for case_group in data:
    for case, items in case_group.items():
        for _, info in items.items():
            product_ids.append(info["상품번호"])

print(product_ids)
# ['2997549821', '2512116583', '3101285106', '2632242759']