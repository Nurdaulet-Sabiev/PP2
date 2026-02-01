a=int(input())
massiv=list(map(int,input().split()))

for i in range(a):
    massiv[i]=massiv[i]*massiv[i]

for i in range(a):
    print(massiv[i],end=" ")