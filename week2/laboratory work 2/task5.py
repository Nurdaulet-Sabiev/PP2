a=int(input())

while a>1:
    if a%2!=0:
        print("NO")
        break
    a=a//2

if(a==1):
    print("YES")