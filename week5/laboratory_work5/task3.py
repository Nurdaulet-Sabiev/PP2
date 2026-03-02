import re

s = input()
pattern = input()

matches = re.findall(pattern, s)
print(len(matches))