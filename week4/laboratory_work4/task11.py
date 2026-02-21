import json

def apply_patch(source, patch):
    for key in patch:

        # 1) если null → удалить
        if patch[key] is None:
            if key in source:
                del source[key]

        # 2) если оба значения — словари → зайти внутрь
        elif key in source and type(source[key]) == dict and type(patch[key]) == dict:
            apply_patch(source[key], patch[key])

        # 3) иначе заменить или добавить
        else:
            source[key] = patch[key]


# читаем вход
source = json.loads(input())
patch = json.loads(input())

# применяем изменения
apply_patch(source, patch)

# печать без пробелов + сортировка
print(json.dumps(source, sort_keys=True, separators=(',', ':')))