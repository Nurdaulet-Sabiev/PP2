import json
import re

data = json.loads(input())
q = int(input())

for _ in range(q):
    query = input()
    cur = data
    ok = True

    # разбиваем путь на части
    parts = re.findall(r'[a-zA-Z_]\w*|\[\d+\]', query)

    for part in parts:
        if part.startswith('['):  # это индекс
            idx = int(part[1:-1])
            if isinstance(cur, list) and 0 <= idx < len(cur):
                cur = cur[idx]
            else:
                ok = False
                break
        else:  # это ключ
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break

    if ok:
        print(json.dumps(cur, separators=(',', ':')))
    else:
        print("NOT_FOUND")