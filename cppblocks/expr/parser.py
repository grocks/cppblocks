'''
A parser for #if/#elif conditional expressions.

The parser is implemented using the Spark GenericParser parser generator.
'''

from ..lib.spark import GenericParser

class astNode:
    def __init__(self, typ, value=None):
        self.typ = typ
        self.value = value
        self.children = []

    def __str__(self, indent=0):
        str = '{0}{1}({2})'.format(indent*' ', self.typ, self.value or '')
        for child in self.children:
            str = '{0}\n{1}'.format(str, child.__str__(indent+1))
        return str

    def __repr__(self):
        return self.__str__();

class astEqualityNode(astNode):
    ' astEquality represents both == and != equality operations '
    def __init__(self, op, lhs, rhs):
        astNode.__init__(self, op)
        self.lhs = lhs
        self.rhs = rhs
        # Append to children for str()/repr()
        self.children.append(lhs)
        self.children.append(rhs)

class astNotNode(astNode):
    def __init__(self, expr):
        astNode.__init__(self, '!')
        self.expr = expr
        # Append to children for str()/repr()
        self.children.append(expr)


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

    def p_defined(self, args):
        '''
            expr ::= defined symbol
        '''
        t = args[1]
        return astNode('defined', t.value)

    def p_not(self, args):
        '''
            expr ::= ! expr
        '''
        return astNotNode(expr=args[1])

    def p_equality(self, args):
        '''
            expr ::= expr == expr
            expr ::= expr != expr
        '''
        opType = args[1].typ
        return astEqualityNode(lhs=args[0], op=opType, rhs=args[2])
