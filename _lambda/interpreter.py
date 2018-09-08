from .lamb_types import LCCall, LCFunction, LCVariable
from .utils import tokenize, pull, LambdaSyntaxError, file2tokens
from .reduce_machine import reduce_machine_low

__version__ = '0.0.1'
__author__ = "zhzLuke96"
__date__ = "Aug 22 16:13:29 2018"


class LCEnv(dict):
    def __init__(self):
        pass


global_env = LCEnv()


def LCDefine(name, exp):
    global global_env
    global_env.update({name: exp})


def LCObjCpy(LCobj):
    return eval_lamb(str(LCobj))


def parse_tokens(tokens):
    exp = []
    while len(tokens) is not 0:
        token = tokens.pop(0)
        if token == "(":
            value = parse_tokens(pull(tokens)[1:-1])
            exp.append(value)
        elif token == ")":
            raise LambdaSyntaxError(
                "Uncaught SyntaxError: Unexpected token )")
            return None
        else:
            exp.append(token)
    return exp


def sign(ast):
    global global_env

    def shiftNone(_l, _r):
        if _l is None and _r is None:
            return None
        elif _l is None:
            return _r
        elif _r is None:
            return _l
        return LCCall(_l, _r)
    if isinstance(ast, str):
        quote = global_env.get(ast)
        if quote is not None:
            return LCObjCpy(quote)
        return LCVariable(ast)
    elif ast[0] in ["boolean", "bool"]:
        TEST = LCCall(LCCall(sign(ast[1:]), "True"), "False")
        TEST_r = reduce_machine_low(TEST)
        if str(TEST_r) == "False":
            return LCVariable("False")
        else:
            return LCVariable("True")
    elif ast[0] in ["define", "def"]:
        LCDefine(ast[1], sign(ast[2:]))
        return None
    elif "." in ast:
        return LCFunction(ast[0], sign(ast[2:]))
    else:
        if len(ast) is 0:
            return None
        elif len(ast) is 1:
            return sign(ast[0])
        elif len(ast) is 2:
            return shiftNone(sign(ast[0]), sign(ast[1]))
        else:
            return shiftNone(sign(ast[:2]), sign(ast[2:]))


def eval_file(filename):
    _ast = parse_tokens(file2tokens(filename))
    return sign(_ast)


def eval_lamb(s_exp):
    _ast = parse_tokens(tokenize(s_exp))
    return sign(_ast)


if __name__ == '__main__':
    print(tokenize("(x.(y.(x y)))"))
    print(eval_lamb("(x.(y.(x y)))"))

    zero = eval_lamb("(f.(x.x))")
    succ = eval_lamb("(n.(f.(x.(f((n f) x)))))")

    # ((f.(x.x)) (n.(f.(x.(f((n f) x))))))
    # ((n.(f.(x.(f((n f) x))))) (f.(x.x)))
    calc = LCCall(succ, zero)
    print(succ, zero, calc)
    from reduce_machine import reduce_machine
    reduce_machine(calc)
