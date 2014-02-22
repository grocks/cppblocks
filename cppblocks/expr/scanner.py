'''
The ExprScanner parses a CPP conditional expression (#if/#elif) and tokenizes it.
'''

from ..lib.spark import GenericScanner

class Token:
    def __init__(self, typ, value=None):
        self.typ = typ
        self.value = value

    def __str__(self):
        return "{0}({1})".format(self.typ, self.value)

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, o):
        return cmp(self.typ, o)

class ExprScanner(GenericScanner):
    def __init__(self):
        GenericScanner.__init__(self)

    def tokenize(self, expression):
        self.rv = []
        GenericScanner.tokenize(self, expression)
        return self.rv

    def t_defined(self, s):
        r'defined'
        self.rv.append(Token('defined', s))

    def t_constant(self, s):
        r'[0-9]+'
        self.rv.append(Token('number', s))

    def t_symbol(self, s):
        r'\b[A-Za-z_][A-Za-z_0-9]*'
        self.rv.append(Token('symbol', s))

    def t_space(self, s):
        r'\s+'
        pass # discard space

