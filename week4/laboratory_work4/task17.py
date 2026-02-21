import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1

# коэффициенты квадратного уравнения
a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - R*R

# длина всего отрезка
length = math.sqrt(a)

D = b*b - 4*a*c

# если нет пересечения с кругом
if D < 0:
    # либо весь внутри, либо весь снаружи
    if x1*x1 + y1*y1 <= R*R:
        print(f"{length:.10f}")
    else:
        print("0.0000000000")
else:
    t1 = (-b - math.sqrt(D)) / (2*a)
    t2 = (-b + math.sqrt(D)) / (2*a)

    # берём только часть внутри отрезка [0, 1]
    left = max(0, min(t1, t2))
    right = min(1, max(t1, t2))

    if left >= right:
        print("0.0000000000")
    else:
        print(f"{length * (right - left):.10f}")