a=int(input())

nums=list(map(int,input().split()))

maxx=nums[0]
minn=nums[0]

for i in nums:
    if(i>maxx):
        maxx=i

for i in nums:
    if(i<minn):
        minn=i
        
for i in range(a):
    if(nums[i]==maxx):
        nums[i]=minn

for i in nums:
    print(i,end=" ")