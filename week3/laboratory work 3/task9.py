class Circle():
    def init(self,radius):
        self.radius=radius
    
    def Area(self):
        pi=3.14159
        ar=pi*(self.radius*self.radius)
        print(f"{ar:.2f}")
    

rad=int(input())
one=Circle(rad)
one.Area()