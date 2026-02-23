"""03_char_classes_quantifiers.py
Наборы символов и квантификаторы {n}, {n,}, {n,m}
"""
import re

s = "aaa abbb aab aaaaab 1234"

# Класс символов: [abc], [a-z]
print("[ab]+:", re.findall(r"[ab]+", s))
print("[0-9]{2,4}:", re.findall(r"[0-9]{2,4}", s))

# {n} — ровно n
print("a{3}:", re.findall(r"a{3}", s))
# {n,} — n и более
print("a{2,}:", re.findall(r"a{2,}", s))
# {n,m} — от n до m
print("a{2,4}:", re.findall(r"a{2,4}", s))

# Пример: валидатор номера (4 цифры)
codes = ["1234", "12", "abcd"]
for c in codes:
    print(c, bool(re.fullmatch(r"\d{4}", c)))

if __name__ == '__main__':
    pass