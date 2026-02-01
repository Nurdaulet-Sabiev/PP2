n=int(input())


arr=[]


for i in range(n):
    word=input()
    arr.append(word)

dictin={}


for i in range(n):
    word=arr[i]
    if word not in dictin:
        dictin[word]=i+1

unique=list(dictin.keys())
unique.sort()



for word in unique:
    print(word, dictin[word])