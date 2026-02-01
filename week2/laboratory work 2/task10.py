a=int(input())

nums=list(map(int,input().split()))

nums.sort(reverse=True)

for i in nums:
    print(i,end=" ")