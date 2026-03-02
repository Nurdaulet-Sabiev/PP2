import re

s = input()

# \b — граница слова, \w{3} — ровно 3 символа
words = re.findall(r'\b\w{3}\b', s)

print(len(words))