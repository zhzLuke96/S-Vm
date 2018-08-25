from lamb_types import LCCall, LCFunction, LCVariable
import regex as re

__version__ = '0.0.1'
__author__ = "zhzLuke96"
__date__ = "Aug 22 16:13:29 2018"


class LCEnv(dict):
    def __init__(self):
        pass


class LambdaSyntaxError(BaseException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


global_env = LCEnv()


def trim(s):
    if len(s) == 0:
        return s
    elif s[0] in " \n\t":
        return (trim(s[1:]))
    elif s[-1] in " \n\t":
        return (trim(s[:-1]))
    return s


def tokenize(string):
    def insterBlank(code):
        return re.sub("([\\.()])", " \\g<1> ", code)
    return list(map(lambda x: re.split("\s+", x), trim(insterBlank(string)).split("\n")))[0]


def pull(tokens):
    subNode = ["("]
    breakCount = 1
    while len(tokens) is not 0:
        token = tokens.pop(0)
        if token == "(":
            breakCount += 1
        elif token == ")":
            breakCount -= 1
        subNode.append(token)
        if breakCount is 0:
            break
    if breakCount is not 0:
        raise LambdaSyntaxError("Uncaught SyntaxError: Unexpected token )")
    return subNode


def LCDefine(name, exp):
    global global_env
    global_env.update({name: exp})


def LCObjCpy(LCobj):
    return eval_lamb(str(LCobj))


def eval_lamb(s_exp):
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
        elif "define" in ast:
            LCDefine(ast[1], sign(ast[2:]))
            return None
        elif "." in ast:
            return LCFunction(ast[0], sign(ast[2:]))
            # return LCFunction(ast[0], sign(ast[2]))
        else:
            # left_associative
            if len(ast) is 0:
                return None
                # raise LambdaSyntaxError(
                #     "Uncaught SyntaxError: Unexpected token ()")
            elif len(ast) is 1:
                return sign(ast[0])
            elif len(ast) is 2:
                return shiftNone(sign(ast[0]), sign(ast[1]))
            else:
                # _left = shiftNone(sign(ast[0]), sign(ast[1]))
                return shiftNone(sign(ast[:2]), sign(ast[2:]))
            # if len(ast) is not 2:
            #     raise LambdaSyntaxError(
            #         f"Uncaught SyntaxError: Unexpected token {ast}")
            # ast = LCCall(sign(ast[0]), sign(ast[1]))
        # return ast
    _ast = parse_tokens(tokenize(s_exp))
    # ast = _ast[0]
    # print(_ast)
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
