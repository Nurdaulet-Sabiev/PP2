d = {
    "ZER": "0",
    "ONE": "1",
    "TWO": "2",
    "THR": "3",
    "FOU": "4",
    "FIV": "5",
    "SIX": "6",
    "SEV": "7",
    "EIG": "8",
    "NIN": "9"
}

rd = {
    "0": "ZER",
    "1": "ONE",
    "2": "TWO",
    "3": "THR",
    "4": "FOU",
    "5": "FIV",
    "6": "SIX",
    "7": "SEV",
    "8": "EIG",
    "9": "NIN"
}

s = input()

# ищем оператор
if "+" in s:
    op = "+"
elif "-" in s:
    op = "-"
else:
    op = "*"

left, right = s.split(op)

# переводим слова в число
num1 = ""
for i in range(0, len(left), 3):
    num1 += d[left[i:i+3]]

num2 = ""
for i in range(0, len(right), 3):
    num2 += d[right[i:i+3]]

a = int(num1)
b = int(num2)

# считаем
if op == "+":
    res = a + b
elif op == "-":
    res = a - b
else:
    res = a * b

# переводим обратно в слова
out = ""
for ch in str(res):
    out += rd[ch]

print(out)
