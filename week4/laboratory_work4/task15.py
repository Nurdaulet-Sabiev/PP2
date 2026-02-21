# Решение для задачи "Next Birthday (Time Zones)"
# Читает 2 строки:
#   1) birth_date_line: "YYYY-MM-DD UTC±HH:MM"
#   2) current_date_line: "YYYY-MM-DD UTC±HH:MM"
# Выводит одно целое — число дней до ближайшего дня рождения (0, если сейчас момент дня рождения).

from os import name
import sys
import datetime
import calendar

def parse_line(line):
    # Возвращает (year, month, day, tzinfo)
    line = line.strip()
    if not line:
        return None
    # Ожидаем: "YYYY-MM-DD UTC+HH:MM" (разделяем по пробелу справа)
    date_part, tz_part = line.rsplit(' ', 1)
    y, m, d = map(int, date_part.split('-'))
    # tz_part like "UTC+05:30" или "UTC-00:45" или "UTC+00:00"
    assert tz_part.startswith('UTC')
    sign = tz_part[3]  # '+' or '-'
    hhmm = tz_part[4:]
    hh, mm = map(int, hhmm.split(':'))
    offset_minutes = hh * 60 + mm
    if sign == '-':
        offset_minutes = -offset_minutes
    tz = datetime.timezone(datetime.timedelta(minutes=offset_minutes))
    return (y, m, d, tz)

def make_birthday_datetime(year, birth_month, birth_day, birth_tz):
    # если день рождения 29 февраля и year не leap => используем 28 февраля
    if birth_month == 2 and birth_day == 29 and not calendar.isleap(year):
        day = 28
    else:
        day = birth_day
    return datetime.datetime(year, birth_month, day, 0, 0, 0, tzinfo=birth_tz)

def main():
    data = sys.stdin.read().strip().splitlines()
    if len(data) < 2:
        return
    birth_line = data[0]
    current_line = data[1]

    by, bm, bd, birth_tz = parse_line(birth_line)
    cy, cm, cd, current_tz = parse_line(current_line)

    # текущий момент: local midnight in current_tz
    current_local = datetime.datetime(cy, cm, cd, 0, 0, 0, tzinfo=current_tz)
    # переводим в UTC for comparison
    current_utc = current_local.astimezone(datetime.timezone.utc)

    # чтобы корректно выбрать год для ближайшего дня рождения, смотрим текущую дату в time zone рождения
    current_in_birth_tz = current_utc.astimezone(birth_tz)
    year0 = current_in_birth_tz.year

    candidates = []
    for y in (year0, year0 + 1):
        bd_dt_birth_tz = make_birthday_datetime(y, bm, bd, birth_tz)  # midnight in birth tz
        bd_dt_utc = bd_dt_birth_tz.astimezone(datetime.timezone.utc)
        if bd_dt_utc >= current_utc:
            candidates.append(bd_dt_utc)
    # Если по какой-то причине оба кандидата < current_utc (маловероятно), добавим следующий год
    if not candidates:
        y = year0 + 2
        bd_dt_birth_tz = make_birthday_datetime(y, bm, bd, birth_tz)
        candidates.append(bd_dt_birth_tz.astimezone(datetime.timezone.utc))

    target = min(candidates)  # ближайший >= current
    delta = target - current_utc
    seconds = int(delta.total_seconds())
    if seconds <= 0:
        print(0)
    else:
        days = (seconds + 86400 - 1) // 86400  # ceil(seconds / 86400) via integer arithmetic
        print(days)


main()