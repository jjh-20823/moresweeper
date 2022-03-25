class test():
    def __init__(self, a) -> None:
        self.a = a

    def check(self, func):
        print(self.a)
        if self.a == 5:
            return
        func()
        print(self.a + 2)

    @check
    def t(self):
        print(self.a + 1)

s = test(2)
s.t()