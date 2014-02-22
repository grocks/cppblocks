'''
A parser for #if/#elif conditional expressions.

The parser is implemented using the Spark GenericParser parser generator.
'''

from ..lib.spark import GenericParser

class astNode:
    def __init__(self, typ, value):
        self.typ = typ
        self.value = value
        self.children = []

    def __str__(self, indent=0):
        str = '{0}{1}({2})'.format(indent*' ', self.typ, self.value)
        for child in self.children:
            str = '{0}\n{1}'.format(str, child.__str__(indent+1))
        return str

    def __repr__(self):
        return self.__str__();

class ExprParser(GenericParser):
    def __init__(self, startToken='expr'):
        GenericParser.__init__(self, startToken)

    def p_number(self, args):
        '''
            expr ::= number
        '''
        t = args[0]
        return astNode('number', t.value)

    def p_symbol(self, args):
        '''
            expr ::= symbol
        '''
        t = args[0]
        return astNode('symbol', t.value)
