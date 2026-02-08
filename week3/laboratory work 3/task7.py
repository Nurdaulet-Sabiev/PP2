import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"({self.x}, {self.y})")

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)


# ввод первой точки
x1, y1 = map(int, input().split())
p1 = Point(x1, y1)

# показать начальные координаты
p1.show()

# перемещение
x2, y2 = map(int, input().split())
p1.move(x2, y2)

# показать новые координаты
p1.show()

# ввод второй точки
x3, y3 = map(int, input().split())
p2 = Point(x3, y3)

# расстояние
d = p1.dist(p2)
print(f"{d:.2f}")
