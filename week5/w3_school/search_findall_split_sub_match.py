"""04_search_findall_split_sub_match.py
re.search, re.findall, re.split, re.sub, re.match
"""
import re

text = "one,two;three four  five"

# search — первое совпадение, возвращает Match
m = re.search(r"t\w+", text)
print("search ->", m.group() if m else None)

# findall — список всех совпадений
print("findall ->", re.findall(r"\w+", text))

# split — разделить по шаблону
print("split ->", re.split(r"[ ,;]+", text))

# sub — заменить
print("sub ->", re.sub(r"\s+", " ", text))

# match — только в начале строки
print("match ->", bool(re.match(r"one", text)))
print("match false ->", bool(re.match(r"two", text)))

if __name__ == '__main__':
    pass