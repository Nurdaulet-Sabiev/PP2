n = int(input())

# создаём массив
lox = [0]*n

# считываем номера
for i in range(n):
    lox[i] = input()

# создаём массив для подсчёта количества каждого номера
count = [0]*n

# считаем частоты
for i in range(n):
    for j in range(n):
        if lox[i] == lox[j]:
            count[i] += 1

num = 3
res = 0

# считаем, сколько разных номеров встречается ровно 3 раза
added = set()  # чтобы не посчитать один номер несколько раз
for i in range(n):
    if count[i] == num and lox[i] not in added:
        res += 1
        added.add(lox[i])

print(res)