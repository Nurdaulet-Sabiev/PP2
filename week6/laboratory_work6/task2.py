# Чтение числа n
n = int(input())

# Чтение n чисел
numbers = map(int, input().split())

# Фильтрация чётных чисел и подсчёт их количества
even_count = len(list(filter(lambda x: x % 2 == 0, numbers)))

# Вывод результата
print(even_count)