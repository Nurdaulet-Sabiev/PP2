a=int(input())

nums=list(map(int,input().split()))

maxx=nums[0]

for i in nums:
    if(i>maxx):
        maxx=i

print(maxx)