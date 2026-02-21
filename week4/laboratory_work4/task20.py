g = 0
n = 0

k = int(input())

for _ in range(k):
    scope, value = input().split()
    value = int(value)

    if scope == "global":
        g += value
    elif scope == "nonlocal":
        n += value
    # local — ничего не делаем

print(g, n)