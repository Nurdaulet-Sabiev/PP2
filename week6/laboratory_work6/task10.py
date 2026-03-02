n = int(input())
numbers = map(int, input().split())

count_truthy = sum(map(bool, numbers))

print(count_truthy)