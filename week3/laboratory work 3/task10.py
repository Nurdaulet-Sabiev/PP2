class Person:
    def init(self, name, gpa):
        self.name = name
        self.gpa = gpa


class Student(Person):
    def init(self, name, gpa):
        super().init(name, gpa)

    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")
        
        
name2,gpa2=input().split()
stud=Student(name2,gpa2)
stud.display()