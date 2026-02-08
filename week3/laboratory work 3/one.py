def checker(num):
    work=True
    
    for i in num:
        if int(i)%2==1:
            work=False
    
    if(work):print("Valid")
    else:print("Not valid")

num2=input()
checker(num2)