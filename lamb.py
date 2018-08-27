import click
import configparser as cp
from _lambda.interpreter import eval_file
from _lambda.repl import repl


def importLib():
    config = cp.SafeConfigParser()
    config.read("./config.ini")
    lamb_import = [i[1] for i in config.items("import")]
    for l in lamb_import:
        _a_ = eval_file(l)


@click.command()
@click.argument('filename', required=False)
@click.option('--mode', default="default", help='Interpreter mode setting:\n\t--Debug Mode: will display all the calculation process;\n\t--Execute Mode: will only display the final result; \n\tdefault is execute mode.')
def welcome(filename, mode):
    """
    Lambda calculus (also written as λ-calculus) is a formal system in mathematical logic for expressing computation based on function abstraction and application using variable binding and substitution. It is a universal model of computation that can be used to simulate any Turing machine. It was first introduced by mathematician Alonzo Church in the 1930s as part of his research of the foundations of mathematics.
    """
    importLib()
    if filename:
        res = eval_file(filename)
        print(res)
    else:
        repl(mode.lower())


if __name__ == '__main__':
    welcome()
