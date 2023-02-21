class Constraint():
    def __init__(self, a: int = 0,  b: int = 0,  r1: int = 0,  r2: int = 0,  r3: int = 0,  r4: int = 0):
        self.a = a
        self.b = b
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4

    def __str__(self) -> str:
        return f"Constraint a={self.a} b={self.b}"
