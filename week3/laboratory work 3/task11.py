class Pair:
    def init(self, a, b):
        self.a = a
        self.b = b

    def add(self, other):
        return Pair(self.a + other.a, self.b + other.b)


# input
a1, b1, a2, b2 = map(int, input().split())

p1 = Pair(a1, b1)
p2 = Pair(a2, b2)

result = p1.add(p2)

print(f"Result: {result.a} {result.b}")