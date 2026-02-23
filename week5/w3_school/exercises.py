"""06_exercises.py
Набор упражнений (варианты):
1) Найти все даты в формате YYYY-MM-DD
2) Заменить несколько пробелов на один
3) Проверить корректность email (упрощенно)
4) Извлечь тэги HTML (простая версия)

Запустите этот файл и посмотрите результаты.
"""
import re

text = "Dates: 2023-08-10, 1999-12-31, wrong: 20230810"
print("dates:", re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text))

s = "This   is   spaced\nNew\tline"
print("normalized spaces:", re.sub(r"\s+", " ", s))

emails = ["user@example.com", "bad@com", "a.b@domain.co"]
for e in emails:
    ok = bool(re.fullmatch(r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}", e))
    print(e, ok)

html = "<div>Hello</div><p>Text</p>"
print("tags:", re.findall(r"<\s*(\w+)[^>]*>", html))

# Упражнение: написать функцию, находящую номера телефонов в тексте

def find_phones(text):
    # шаблон допускает разные разделители и +7/7/8
    return re.findall(r"(?:\+7|7|8)?[\s-]?(?:\(?\d{3}\)?)[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}", text)

print(find_phones("Call +7 (701) 123-45-67 or 87011234567"))

if __name__ == '__main__':
    pass