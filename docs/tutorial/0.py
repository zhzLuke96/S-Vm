class LCVariable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class LCFunction:
    def __init__(self, para, body):
        self.para = para
        self.body = body

    def __str__(self):
        return f"({self.para}.{self.body})"


class LCCall:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.right})"


if __name__ == '__main__':
    # one
    print(LCFunction("f",
                     LCFunction("x",
                                LCCall(
                                    LCVariable("f"), LCVariable("x")
                                ))))
