n = int(input())

db = {}

for i in range(n):

    line = input().split()

    if line[0] == "set":
        key = line[1]
        value = line[2]
        db[key] = value

    if line[0] == "get":
        key = line[1]

        if key in db:
            print(db[key])
        else:
            print("KE: no key", key, "found in the document")