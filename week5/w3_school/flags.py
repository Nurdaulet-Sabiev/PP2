"""05_flags.py
Флаги: IGNORECASE, MULTILINE, DOTALL, VERBOSE
"""
import re

s = "Start\nline Two\nLINE THREE"

# IGNORECASE
print("ignorecase:", re.findall(r"line", s, flags=re.IGNORECASE))

# MULTILINE — ^ и $ работают на каждой строке
print("multiline ^line:", re.findall(r"^line", s, flags=re.MULTILINE | re.IGNORECASE))

# DOTALL — . захватывает и переводы строки
print("dotall:", re.findall(r"Start.*THREE", s, flags=re.DOTALL | re.IGNORECASE))

# VERBOSE — удобный формат для сложных шаблонов
pattern = re.compile(r"""
    \b   # граница слова
    \d{3} -? \d{2}  # пример: 123-45 или 12345
    \b
""", flags=re.VERBOSE)
print(pattern.findall("code 123-45 and 67890"))

if __name__ == '__main__':
    pass