class Shape:
    def area(self):
        return 0
    
class rectangle:
    def __init__(self,length,width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width
    
    
l, w = map(int, input().split())

r = rectangle(l, w)
print(r.area())