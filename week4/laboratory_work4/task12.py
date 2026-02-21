import json

def find_diff(a, b, path, result):
    keys = set(a.keys()) | set(b.keys())

    for key in keys:
        new_path = key if path == "" else path + "." + key

        if key not in a:
            result.append(f"{new_path} : <missing> -> {json.dumps(b[key], separators=(',', ':'))}")

        elif key not in b:
            result.append(f"{new_path} : {json.dumps(a[key], separators=(',', ':'))} -> <missing>")

        elif isinstance(a[key], dict) and isinstance(b[key], dict):
            find_diff(a[key], b[key], new_path, result)

        elif a[key] != b[key]:
            result.append(
                f"{new_path} : {json.dumps(a[key], separators=(',', ':'))} -> {json.dumps(b[key], separators=(',', ':'))}"
            )


# читаем JSON
a = json.loads(input())
b = json.loads(input())

result = []
find_diff(a, b, "", result)

if not result:
    print("No differences")
else:
    for line in sorted(result):
        print(line)