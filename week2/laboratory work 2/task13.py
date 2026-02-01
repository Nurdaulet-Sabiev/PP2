n=int(input())


if n<=1:
    print("No")
else:
    prime=True
    
    i=2
    
    while i*i<=n:
        if n%i==0:
            prime=False
            break
        i+=1
       
        
if prime:
    print("Yes")
else:
    print("No")