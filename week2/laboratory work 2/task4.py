a=int(input())

nums=list(map(int,input().split()))

pos=0

for i in nums:
    if(i>0):
        pos+=1
        
print(pos)