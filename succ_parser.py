from errors import InvalidSyntaxtError
from nodes import NumberNode, BinOpNode, UnaryOpNode
from tokens import TT_DIV, TT_EOF, TT_FLOAT, TT_INT, TT_LPAREN, TT_MINUS, TT_MUL, TT_PLUS, TT_RPAREN

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]
        return self.current_token

    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxtError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected '+', '-', '*' or '/'"
            ))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.current_token

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expres = res.register(self.expr())
            if res.error: return res
            if self.current_token.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expres)
            else:
                return res.failure(InvalidSyntaxtError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))
                
        return res.failure(InvalidSyntaxtError(
            tok.pos_start, tok.pos_end, "Expected int or float \n"
        ))

    def term(self):
        return self.binary_opeartion(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.binary_opeartion(self.term, (TT_PLUS, TT_MINUS))

    def binary_opeartion(self, func, lis_ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_token.type in lis_ops:
            op_tok = self.current_token
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)