import re

s = input()

uppercase_letters = re.findall(r'[A-Z]', s)
print(len(uppercase_letters))