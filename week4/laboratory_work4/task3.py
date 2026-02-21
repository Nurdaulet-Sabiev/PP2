a = int(input())

for i in range(0,a+1):
    if i==0:
        print(i,end=" ")
    elif i%3==0 and i%4==0:
        print(i,end=" ")