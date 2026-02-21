a = int(input())

first = True
for i in range(0, a + 1, 2):
    if not first:
        print(",", end="")
    print(i, end="")
    first = False
