n, l, r = map(int, input().split())
new=list(map(int,input().split()))

l-=1
r-=1

new[l:r+1]=new[l:r+1][::-1]

for i in range(n):
    print(new[i],end=" ")