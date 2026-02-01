n = int(input())
massiv = list(map(int, input().split()))

count = [0] * n

for i in range(n):
    for j in range(n):
        if massiv[i] == massiv[j]:
            count[i] += 1

maxx = count[0]
for i in range(n):
    if count[i] > maxx:
        maxx = count[i]

bigg = 10**18

for i in range(n):
    if count[i] == maxx:
        if massiv[i] < bigg:
            bigg = massiv[i]

print(bigg)
