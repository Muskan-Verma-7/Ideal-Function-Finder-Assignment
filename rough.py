class Testing:
    def __init__(self, a, b, c, d):
        self.a=a
        self.b=b
        self.c=c
        self.d=d

    def calculate(self):
        self.addition = self.a + self.b + self.c + self.d
        self.subtraction = self.a - self.b

        return self.addition, self.subtraction
    
