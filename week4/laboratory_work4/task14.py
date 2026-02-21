from datetime import datetime, timedelta

def parse(line):
    date_part, tz_part = line.split()

    # дата = локальная полночь
    dt = datetime.strptime(date_part, "%Y-%m-%d")

    # UTC±HH:MM
    sign = 1 if tz_part[3] == '+' else -1
    hours = int(tz_part[4:6])
    minutes = int(tz_part[7:9])

    offset = timedelta(hours=hours, minutes=minutes) * sign

    # перевод в UTC
    return dt - offset


d1 = parse(input())
d2 = parse(input())

# ПРАВИЛЬНО: считаем по секундам
seconds = abs((d1 - d2).total_seconds())
days = int(seconds // 86400)

print(days)