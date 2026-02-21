def primes(n):
    for num in range(2, n+1):  # перебираем числа от 2 до n
        is_prime = True
        for i in range(2, int(num**0.5)+1):  # проверка делителей
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            yield num  # если простое, возвращаем число


n = int(input())

result = []
for p in primes(n):
    result.append(str(p))

print(" ".join(result))
