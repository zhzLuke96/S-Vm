from .interpreter import eval_lamb, __version__, __date__, LambdaSyntaxError
from .reduce_machine import reduce_machine, preCalc
from .colorOut import printDarkPink, printDarkYellow


def renameLog(logs):
    for k, v in logs:
        if v[0] is "f":
            printDarkYellow(f"@ >> unbound free variable: {k} rename as {v}\n")
        else:
            printDarkPink(f"$ >> unbound variable: {k} rename as {v}\n")


def read_oneLine(prompt="  >> ", isloging=True):
    try:
        exp = input(prompt)
        # if exp[0] is ":":
        #     exec(exp[1:])
        #     return
        r = eval_lamb(exp)
        # print("i >>", r)
        rn, _ = preCalc(r)
        if isloging and len(_) is not 0:
            renameLog(_)
        reduce_machine(rn, isloging)
    except (KeyboardInterrupt, LambdaSyntaxError) as e:
        print(e)
        if isinstance(e, KeyboardInterrupt):
            exit()
    finally:
        pass


def repl(MODETYPE):
    global __version__, __date__
    print(f"""
- lambda interpreter {__version__} ({MODETYPE}, {__date__})
- Type "help", "copyright", "credits" or "license" for more information.
    """)
    while True:
        read_oneLine(isloging=True if MODETYPE.lower() == "debug" else False)


# ((f.(x.x)) (n.(f.(x.(f((n f) x))))))
# ((n.(f.(x.(f((n f) x))))) (f.(x.x)))

# add := (m.(n.((n (n.(p.(x.(p ((n p) x))))) m))))
# one := (p.(x.(p x)))

# test case
# (add one) one
# (((m.(n.((n (n.(p.(x.(p ((n p) x)))))) m))) (p.(x.(p x)))) (p.(x.(p x))))

# (f.(x.(f (x x))))

# Y
# (y.((x.(y(x x))) (x.(y(x x)))))
# boom!
if __name__ == '__main__':
    repl()
