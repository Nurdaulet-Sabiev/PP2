nums = list(map(int, input().split()))

def is_prime(x):
    if x <= 1:
        return False
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            return False
    return True

primes = list(filter(is_prime, nums))

if len(primes) == 0:
    print("No primes")
else:
    for p in primes:
        print(p, end=" ")
