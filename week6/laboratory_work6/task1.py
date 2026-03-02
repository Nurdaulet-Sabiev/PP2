# Чтение числа n
n = int(input())

# Чтение n чисел и преобразование их в список целых чисел
numbers = map(int, input().split())

# Вычисление суммы квадратов
sum_of_squares = sum(map(lambda x: x**2, numbers))

# Вывод результата
print(sum_of_squares)