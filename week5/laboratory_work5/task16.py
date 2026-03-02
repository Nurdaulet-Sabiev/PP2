import re

s = input()

match = re.match(r'Name: (.+), Age: (.+)', s)
if match:
    print(match.group(1), match.group(2))