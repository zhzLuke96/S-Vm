class LCVariable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name.__str__()

    def replace(self, name, replacement):
        if self.name is name:
            return replacement
        return self


class LCFunction:
    def __init__(self, para, body):
        self.para = para
        self.body = body

    def __str__(self):
        return f"({self.para}.{self.body})"

    def replace(self, name, replacement):
        if self.para is name:
            return self
        else:
            return LCFunction(self.para, self.body.replace(name, replacement))


class LCCall:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.right})"

    def replace(self, name, replacement):
        return LCCall(self.left.replace(name, replacement),
                      self.right.replace(name, replacement))


if __name__ == '__main__':
    # one
    print(LCFunction("f",
                     LCFunction("x",
                                LCCall(
                                    LCVariable("f"), LCVariable("x")
                                ))))
    # x
    expression = LCVariable("x")
    print(expression)

    expression.replace("x",
                       LCFunction("y", LCVariable("y")))
    print(expression)

    expression.replace("z",
                       LCFunction("y", LCVariable("y")))
    print(expression)

    expression = LCCall(LCCall(
        LCCall(LCVariable("a"), LCVariable("b")),
        LCVariable("c")
    ), LCVariable("b"))
    print(expression)

    expression.replace("b", LCFunction("x", LCVariable("x")))
    print(expression)

    expression = LCFunction("y", LCCall(LCVariable("x"), LCVariable("y")))
    print(expression)
    expression.replace("x", LCVariable("z"))
    print(expression)
    expression.replace("y", LCVariable("x"))
    print(expression)
    expression.replace("z", LCVariable("y"))
    print(expression)

    # bug 1
    expression = LCFunction("x", LCCall(LCVariable("x"), LCVariable("y")))
    print(expression)
    repl = LCCall(LCVariable("z"), LCVariable("x"))
    expression.replace("y", repl)
    print(expression)
    # freeX is not x
