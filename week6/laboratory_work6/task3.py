n = int(input())
words = input().split()
result = []

for index, word in enumerate(words):
    pair = str(index) + ":" + word
    result.append(pair)

output = " ".join(result)
print(output)