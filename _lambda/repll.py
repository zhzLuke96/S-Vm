from __future__ import unicode_literals
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
# from pygments.lexers.lisp import SchemeLexer
from .utils import fuzzyfinder
from .interpreter import eval_lamb, __version__, __date__
from .reduce_machine import reduce_machine, preCalc
from .interpreter import global_env
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from .colorOut import printDarkPink, printDarkYellow

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#ffffff',
})

eval_keywords = ["define", "def", "boolean", "bool", ]


class lambdaCompleter(Completer):
    def get_completions(self, document, complete_event):
        global global_env
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor,
                              list(global_env.keys()) + eval_keywords, ignore_case=True)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


def renameLog(logs):
    for k, v in logs:
        if v[0] is "f":
            printDarkYellow(f"@ >> unbound free variable: {k} rename as {v}\n")
        else:
            printDarkPink(f"$ >> unbound variable: {k} rename as {v}\n")


def main(mode="debug"):
    global __version__, __date__
    print(f"""
- lambda interpreter {__version__} ({mode}, {__date__})
- Type "help", "copyright", "credits" or "license" for more information.
    """)
    session = PromptSession(
        history=FileHistory("history.txt"),
        auto_suggest=AutoSuggestFromHistory(),
        # lexer=PygmentsLexer(SchemeLexer),
        completer=lambdaCompleter(), style=style)
    isloging = True if mode.lower() == "debug" else False
    while True:
        try:
            exp = session.prompt('  >> ')
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        else:
            r = eval_lamb(exp)
            rn, rename = preCalc(r)
            if isloging and len(rename) is not 0:
                renameLog(rename)
            reduce_machine(rn, rename, isloging)
    print('exit!')
