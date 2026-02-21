import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1

AB = math.hypot(dx, dy)

# расстояния от центра
d1 = math.hypot(x1, y1)
d2 = math.hypot(x2, y2)

# параметр проекции центра (0,0) на отрезок AB
t = -(x1*dx + y1*dy) / (AB*AB)

# если проекция вне отрезка — идём напрямую
if t < 0 or t > 1:
    print(f"{AB:.10f}")
    exit()

# расстояние от центра до отрезка
area = abs(x1*y2 - y1*x2)
h = area / AB

# если отрезок не заходит в круг
if h >= R:
    print(f"{AB:.10f}")
    exit()

# ---- путь вокруг круга ----

t1 = math.sqrt(d1*d1 - R*R)
t2 = math.sqrt(d2*d2 - R*R)

a1 = math.acos(R / d1)
a2 = math.acos(R / d2)

dot = x1*x2 + y1*y2
angle = math.acos(dot / (d1 * d2))

arc = angle - a1 - a2

path = t1 + t2 + R * arc

print(f"{path:.10f}")
