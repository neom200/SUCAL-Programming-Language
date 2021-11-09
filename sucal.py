from lexer import Lexer
from succ_parser import Parser
from intepreter import Interpreter
from context import Context, SymbolTable
from numero import Number
import sys

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number(0))
global_symbol_table.set("TRUE", Number(1))
global_symbol_table.set("FALSE", Number(0))

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run the AST
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

def runFromFile(filename):
    if filename.find('.succ') == -1:
        print(f"ERROR: {filename} doesn't have a appropriate extension")
        return

    nome = filename.split('.')[0]
    with open(filename, 'r') as f:
        full_text = f.read()
        all_lines = full_text.split('\n')

        for lines in all_lines:
            result, erro = run(f'<{nome}>', lines)

            if erro: print(erro.as_string())
            else: print(result)

def runFromStdin():
    while True:
        text = input('sucal >> ')

        if text == 'exit()':
            break

        result, erro = run('<stdin>', text)

        if erro: print(erro.as_string())
        else: print(result)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'stdin'
    
    if filename == 'stdin':
        runFromStdin()
    else:
        runFromFile(filename)