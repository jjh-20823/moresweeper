# class test():
#     def __init__(self, a) -> None:
#         self.a = a

#     def check(self, func):
#         print(self.a)
#         if self.a == 5:
#             return
#         func()
#         print(self.a + 2)

#     @check
#     def t(self):
#         print(self.a + 1)

# s = test(2)
# s.t()


class aaa():
    def __init__(self):
        self.a = -2
    def w(func):
        def wh(self, b, c):
            if self.a >= 0:
                print(666)
                func(self, b, c)
                return
            else:
                print(555)
                func(self, b, c)
                return
        return wh
    @w
    def h(self, bb, cc):
        print(88, bb, cc)
        self.a += 1
A = aaa()
A.h(4, 7)
A.h(4, 7)
A.h(4, 7)
A.h(4, 7)