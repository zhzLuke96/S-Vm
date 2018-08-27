__version__ = '0.0.1'
__author__ = "zhzLuke96"
__date__ = "18/08/22"


class LCVariable:
    def __init__(self, name):
        self.name = name
        self.isfree = True

    def __str__(self):
        return str(self.name)

    def bind(self, name, replacement):
        if self.name is name:
            self.isfree = False
            self.name = replacement

    def replace(self, name, replacement):
        if self.name is name:
            return replacement
        return self

    def reducible(self):
        return False


class LCFunction:
    # callable = True
    def __init__(self, para, body):
        self.para = para
        self.body = body

    def __str__(self):
        return f"({self.para}.{self.body})"

    def __call__(self, argument):
        return self.body.replace(self.para, argument)

    def bind(self, name, replacement):
        if self.para is name:
            self.para = replacement
        self.body.bind(name, replacement)

    def replace(self, name, replacement):
        if self.para is name:
            return self
        else:
            return LCFunction(self.para, self.body.replace(name, replacement))

    def reducible(self):
        return self.body.reducible()

    def reduce(self):
        if self.body.reducible():
            return LCFunction(self.para, self.body.reduce())
        return self


class LCCall:
    reducible = True

    def __init__(self, left, right):
        self.left = left if not isinstance(left, str) else LCVariable(left)
        self.right = right if not isinstance(right, str) else LCVariable(right)

    def __str__(self):
        return f"({self.left} {self.right})"

    def bind(self, name, replacement):
        self.left.bind(name, replacement)
        self.right.bind(name, replacement)

    def replace(self, name, replacement):
        return LCCall(self.left.replace(name, replacement),
                      self.right.replace(name, replacement))

    def reducible(self):
        return self.left.reducible() or self.right.reducible() or callable(self.left)

    def reduce(self):
        if self.left.reducible():
            if callable(self.left):
                # Lazy Evaluation
                return self.left(self.right)
            else:
                return LCCall(self.left.reduce(), self.right)
        elif self.right.reducible():
            return LCCall(self.left, self.right.reduce())
        else:
            return self.left(self.right)


if __name__ == '__main__':
    # call
    function1 = LCFunction("x", LCFunction(
        "y", LCCall(LCVariable("x"), LCVariable("y"))))
    print(function1)
    arg1 = LCFunction("z", LCVariable("z"))
    res = function1(arg1)
    print(res)

    succ = LCFunction("n", LCFunction("p", LCFunction("x", LCCall(LCVariable(
        "p"), LCCall(LCCall(LCVariable("n"), LCVariable("p")), LCVariable("x"))))))
    # (n.(p.(x.(p ((n p) x)))))

    one = LCFunction("p", LCFunction(
        "x", LCCall(LCVariable("p"), LCVariable("x"))))
    # (p.(x.(p x)))
    add = LCFunction("m", LCFunction("n", LCCall(
        LCCall(LCVariable("n"), succ), LCVariable("m"))))
    # (m.(n.((n succ) m)))
    # (m.(n.((n (n.(p.(x.(p ((n p) x))))) m))))
    # one add one
    expression = LCCall(LCCall(add, one), one)
    while expression.reducible():
        print("reduce>>", expression)
        expression = expression.reduce()
    print(expression)
    # reduce is not fill,now

    expression = LCCall("x", "i")
    print(expression, type(expression.left))

    # bind
    expression = LCFunction("n", LCFunction("p", LCFunction("x", LCCall(LCVariable(
        "p"), LCCall(LCCall(LCVariable("n"), LCVariable("p")), LCVariable("x"))))))
    expression.bind("n", "n1")
    print(expression)
    expression.bind("n1", "n")
    print(expression)

    expression = LCFunction("m", LCCall(expression, expression))
    print(expression)
