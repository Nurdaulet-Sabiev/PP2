n = int(input())
keys = input().split()
values = input().split()
query = input()

my_dict = dict(zip(keys, values))

print(my_dict.get(query, "Not found"))