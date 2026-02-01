n=int(input())

dor={}

for i in range(n):
    n,c=input().split()
    c=int(c)
    
    if n in dor:
        dor[n]=dor[n]+c
    else:
        dor[n]=c


new=list(dor.keys())
new.sort()

for name in new:
    print(name,dor[name])