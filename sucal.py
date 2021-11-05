from lexer import Lexer
from succ_parser import Parser

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error


while True:
    text = input('sucal >> ')

    if text == 'exit()':
        break

    result, erro = run('<stdin>', text)

    if erro: print(erro.as_string())
    else: print(result)
    