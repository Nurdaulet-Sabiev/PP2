a=int(input())

nums=list(map(int,input().split()))

maxx=nums[0]


for i in nums:
    if(i>maxx):
        maxx=i


for i in range(a):
    if(maxx==nums[i]):
        print(i+1)