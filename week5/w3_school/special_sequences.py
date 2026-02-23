"""02_special_sequences.py
Специальные последовательности: \d, \w, \s, \D, \W, \S, \A, \Z
"""
import re

s = "User_01: John_Doe, score: 98, date: 2023-08-10"

print("\d (digits):", re.findall(r"\d+", s))
print("\w (word chars):", re.findall(r"\w+", s))
print("\s (spaces):", re.findall(r"\s+", s))

print("\D (non-digits):", re.findall(r"\D+", "abc123def"))
print("\W (non-word):", re.findall(r"\W+", "hello, world!"))
print("\S (non-space):", re.findall(r"\S+", "a b  c"))

# \A — начало всей строки; \Z — конец всей строки
multi = "first line\nsecond line"
print("\Afirst:", re.findall(r"\Afirst", multi))
print("second\Z:", re.findall(r"second\Z", multi))

if __name__ == '__main__':
    pass