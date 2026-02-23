"""01_metacharacters.py
Примеры метасимволов: ., *, +, ?, ^, $, [], |, (), \\ (экранирование)
"""
import re

s = "cat, cot, cut, caaat, cccat, 123"

# .  — любой символ (кроме перевода строки)
print(". matches:", re.findall(r"c.t", s))

# *  — 0 или более повторений предыдущего токена
print("a*:", re.findall(r"ca*t", s))

# +  — 1 или более
print("a+:", re.findall(r"ca+t", s))

# ?  — 0 или 1
print("o?:", re.findall(r"co?t", s))

# ^ и $  — начало и конец строки
lines = "first\nsecond"
print("^second multiline?:", re.findall(r"^second", lines))

# []  — набор символов
print("[ou]:", re.findall(r"c[ou]t", s))

# |  — альтернативы
print("cat|cot:", re.findall(r"cat|cot", s))

# ()  — группировка
print("(a+):", re.findall(r"c(a+)t", s))

# Экранирование
print("\$ пример:", re.findall(r"\d+", "Стоимость: $100"))

if __name__ == '__main__':
    pass