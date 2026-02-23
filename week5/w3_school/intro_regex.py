"""00_intro_regex.py
Краткое введение в регулярные выражения (re). Примеры: поиск, компиляция, простые шаблоны.
Запустите: python 00_intro_regex.py
"""
import re

text = "My phone: +7-701-123-45-67, email: student@example.com, id: 42"

# Найти первое число
m = re.search(r"\d+", text)
print("Первое найденное число:", m.group() if m else None)

# Найти все email-подобные фрагменты (очень простая шаблонная проверка)
emails = re.findall(r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}", text)
print("Emails:", emails)

# Компиляция шаблона для многократного использования
phone_re = re.compile(r"\+?\d[\d\- ]{7,}\d")
print("Телефоны:", phone_re.findall(text))

if __name__ == '__main__':
    pass