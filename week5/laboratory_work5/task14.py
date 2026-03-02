import re

s = input()

pattern = re.compile(r'^\d+$')  # ^ начало строки, \d+ одна или более цифр, $ конец строки

if pattern.fullmatch(s):
    print("Match")
else:
    print("No match")