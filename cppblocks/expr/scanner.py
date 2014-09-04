'''
The ExprScanner parses a CPP conditional expression (#if/#elif) and tokenizes it.
'''

import trace
def log(*args):
    trace.trace('cppblocks.expr.scanner', *args)

from ..lib.spark import GenericScanner

class Token:
    def __init__(self, typ, value=None):
        self.typ = typ
        self.value = value

    def __str__(self, indent=0):
        if self.value:
            return "{0}{1}({2})".format(indent*' ', self.typ, self.value)
        else:
            return "{0}{1}".format(indent*' ', self.typ)

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, o):
        return cmp(self.typ, o)

class NumberToken(Token):
    def __init__(self, value):
        Token.__init__(self, 'number', value)

class SymbolToken(Token):
    def __init__(self, value):
        Token.__init__(self, 'symbol', value)

CONSTANT_ZERO = NumberToken('0')
CONSTANT_ONE = NumberToken('1')

OP_PLUS = Token('+')
OP_MUL = Token('*')

class ExprScanner(GenericScanner):
    def __init__(self):
        GenericScanner.__init__(self)

    def tokenize(self, expression):
        self.rv = []
        GenericScanner.tokenize(self, expression)
        return self.rv

    def t_defined(self, s):
        r'\bdefined\b'
        self.rv.append(Token('defined'))

    def t_constant(self, s):
        r'[0-9]+'
        self.rv.append(NumberToken(s))

    def t_symbol(self, s):
        r'\b[A-Za-z_][A-Za-z_0-9]*\b'
        self.rv.append(SymbolToken(s))

    def t_equality(self, s):
        r'=='
        self.rv.append(Token('=='))

    def t_inequality(self, s):
        r'!='
        self.rv.append(Token('!='))

    def t_not(self, s):
        r'!'
        self.rv.append(Token('!'))

    def t_lparen(self, s):
        r'\('
        self.rv.append(Token('('))

    def t_rparen(self, s):
        r'\)'
        self.rv.append(Token(')'))

    def t_or(self, s):
        r'\|\|'
        self.rv.append(Token('||'))

    def t_and(self, s):
        r'&&'
        self.rv.append(Token('&&'))

    def t_plus(self, s):
        r'\+'
        self.rv.append(Token('+'))

    def t_minus(self, s):
        r'-'
        self.rv.append(Token('-'))

    def t_mul(self, s):
        r'\*'
        self.rv.append(Token('*'))

    def t_div(self, s):
        r'/'
        self.rv.append(Token('/'))

    def t_space(self, s):
        r'\s+'
        pass # discard space

    def t_default(self, s):
        from ..messages import UnsupportedToken
        log('unsupported token: ' + str(s))
        raise UnsupportedToken(s)
