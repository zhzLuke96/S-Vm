from interpreter import eval_lamb, __version__, __date__, LambdaSyntaxError
from reduce_machine import reduce_machine, preCalc
from colorOut import printDarkPink, printDarkYellow

# default reduce calc editor
MODETYPE = "default"

welcomeText = f"""
- lambda interpreter {__version__} (${MODETYPE}, {__date__})
- Type "help", "copyright", "credits" or "license" for more information.
"""


def renameLog(logs):
    for k, v in logs:
        if v[0] is "f":
            printDarkYellow(f"@ >> unbound free variable: {k} rename as {v}\n")
        else:
            printDarkPink(f"$ >> unbound variable: {k} rename as {v}\n")


def repl():
    def read_oneLine(prompt="  >> "):
        try:
            exp = input(prompt)
            r = eval_lamb(exp)
            rn, _ = preCalc(r)
            if len(_) is not 0:
                renameLog(_)
            print("i >>", rn)
            reduce_machine(rn)
        except (KeyboardInterrupt, LambdaSyntaxError) as e:
            print(e)
            if isinstance(e, KeyboardInterrupt):
                exit()
        finally:
            pass
    while True:
        read_oneLine()


# ((f.(x.x)) (n.(f.(x.(f((n f) x))))))
# ((n.(f.(x.(f((n f) x))))) (f.(x.x)))

# add := (m.(n.((n (n.(p.(x.(p ((n p) x))))) m))))
# one := (p.(x.(p x)))

# test case
# (add one) one
# (((m.(n.((n (n.(p.(x.(p ((n p) x)))))) m))) (p.(x.(p x)))) (p.(x.(p x))))

# (f.(x.(f (x x))))

# Y
# (y.(x.(y(x x)) (x.(y(x x)))))
if __name__ == '__main__':
    print(welcomeText)
    repl()
