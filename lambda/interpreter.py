from lamb_types import LCCall, LCFunction, LCVariable, reduce_machine
import regex as re

__version__ = '0.0.1'
__author__ = "zhzLuke96"
__date__ = "18/08/22"


def trim(s):
    if len(s) == 0:
        return s
    elif s[0] in " \n\t":
        return (trim(s[1:]))
    elif s[-1] in " \n\t":
        return (trim(s[:-1]))
    return s


class LambdaSyntaxError(BaseException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


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
        if isinstance(ast, str):
            return LCVariable(ast)
        elif "." in ast:
            ast = LCFunction(ast[0], sign(ast[2]))
        else:
            ast = LCCall(sign(ast[0]), sign(ast[1]))
        return ast
    ast = parse_tokens(tokenize(s_exp))[0]
    signed = sign(ast)
    return signed


if __name__ == '__main__':
    print(tokenize("(x.(y.(x y)))"))
    print(eval_lamb("(x.(y.(x y)))"))

    zero = eval_lamb("(f.(x.x))")
    succ = eval_lamb("(n.(f.(x.(f((n f) x)))))")

    calc = LCCall(succ, zero)
    print(succ, zero, calc)
    reduce_machine(calc)
