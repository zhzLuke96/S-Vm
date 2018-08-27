from .colorOut import printDarkGray, printDarkGreen
from .lamb_types import LCCall, LCFunction, LCVariable


def reduce_machine(expression, isloging=True):
    while expression.reducible():
        if isloging:
            printDarkGray("= >> " + str(expression) + "\n")
        expression = expression.reduce()
    printDarkGreen(": >> " + str(expression) + "\n")


def preCalc(LCOBJ):
    if LCOBJ is None:
        # exp is ()
        return LCVariable("[__LCNone__]"), []

    counter = dict(bound=0, free=0)
    log = []

    def named(obj, scope):
        if isinstance(obj, LCVariable):
            if obj.name in scope and obj.isfree:
                counter["free"] += 1
                boundName = "f" + str(counter["free"])
                log.append([obj.name, boundName])
                obj.bind(obj.name, boundName)
            return obj
        elif isinstance(obj, LCCall):
            # left = named(obj.left, scope)
            return LCCall(named(obj.left, scope), named(obj.right, scope))
        else:
            if obj.para in scope:
                counter["bound"] += 1
                boundName = "b" + str(counter["bound"])
                log.append([obj.para, boundName])
                obj.bind(obj.para, boundName)
            else:
                obj.bind(obj.para, obj.para)
                scope.append(obj.para)
            return LCFunction(obj.para, named(obj.body, scope))
    return named(LCOBJ, []), log


if __name__ == '__main__':
    # f((x.x(f x))) x
    expression = LCCall(LCFunction("f", LCFunction(
        "x", LCCall("x", LCCall("f", LCCall("g", "x"))))), "x")
    print(expression)
    expression, relog = preCalc(expression)
    print(expression, relog)

    succ = LCFunction("n", LCFunction("p", LCFunction("x", LCCall(LCVariable(
        "p"), LCCall(LCCall(LCVariable("n"), LCVariable("p")), LCVariable("x"))))))
    # (n.(p.(x.(p ((n p) x)))))
    one = LCFunction("p", LCFunction(
        "x", LCCall(LCVariable("p"), LCVariable("x"))))
    # (p.(x.(p x)))
    add = LCFunction("m", LCFunction("n", LCCall(
        LCCall(LCVariable("n"), succ), LCVariable("m"))))
    # (m.(n.((n succ) m)))
    # (m.(n.((n (n.(p.(x.(p ((n p) x)))))) m)))
    # one add one
    expression = LCCall(LCCall(add, one), one)
    expression, relog = preCalc(expression)
    print(relog)
    while expression.reducible():
        print(" >>", expression)
        expression = expression.reduce()
    print(expression)
