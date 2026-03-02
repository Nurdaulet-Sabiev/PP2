import re

s = input()
pattern = input()

escaped_pattern = re.escape(pattern)
matches = re.findall(escaped_pattern, s)
print(len(matches))