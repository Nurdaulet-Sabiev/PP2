import sys
import datetime

def parse_datetime(line):
    line = line.strip()
    # "YYYY-MM-DD HH:MM:SS UTC±HH:MM"
    date_part, time_part, tz_part = line.split(' ')
    y, m, d = map(int, date_part.split('-'))
    hh, mm, ss = map(int, time_part.split(':'))
    # tz_part like "UTC+03:00"
    assert tz_part.startswith('UTC')
    sign = tz_part[3]
    tz_h, tz_m = map(int, tz_part[4:].split(':'))
    offset_minutes = tz_h * 60 + tz_m
    if sign == '-':
        offset_minutes = -offset_minutes
    tzinfo = datetime.timezone(datetime.timedelta(minutes=offset_minutes))
    return datetime.datetime(y, m, d, hh, mm, ss, tzinfo=tzinfo)

def main():
    data = sys.stdin.read().strip().splitlines()
    start = parse_datetime(data[0])
    end = parse_datetime(data[1])
    # переводим оба момента в UTC
    start_utc = start.astimezone(datetime.timezone.utc)
    end_utc = end.astimezone(datetime.timezone.utc)
    delta = end_utc - start_utc
    print(int(delta.total_seconds()))


main()