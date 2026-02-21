x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

# отражаем точку B относительно оси Ox
y2 = -y2

# параметр t, при котором y = 0
t = -y1 / (y2 - y1)

# координата x точки отражения
x = x1 + t * (x2 - x1)

print(f"{x:.10f} 0.0000000000")