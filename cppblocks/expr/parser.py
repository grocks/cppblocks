'''
A parser for #if/#elif conditional expressions.

The parser is implemented using the Spark GenericParser parser generator.
'''

from ..lib.spark import GenericParser

from copy import copy

from scanner import CONSTANT_ZERO, CONSTANT_ONE, OP_PLUS, OP_MUL

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

class astAtomNode(astNode):
    ' represents either a constant or a symbol, e.g., 3, 2, FOOBAR. '
    def __init__(self, value):
        astNode.__init__(self, 'atom', value)

class astBinaryOpNode(astNode):
    ' astBinaryOpNode represents binary operations like +,-,*,/ '
    def __init__(self, typ, lhs, rhs, op):
        astNode.__init__(self, 'binOp')
        self.typ_str = typ
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        # Append to children for str()/repr()
        self.children.append(lhs)
        self.children.append(rhs)

class astSumNode(astBinaryOpNode):
    ' represents both + and - operations '
    def __init__(self, typ, lhs, rhs, op):
        astBinaryOpNode.__init__(self, typ, lhs, rhs, op)

class astProductNode(astBinaryOpNode):
    ' represents both * and / operations '
    def __init__(self, typ, lhs, rhs, op):
        astBinaryOpNode.__init__(self, typ, lhs, rhs, op)

class astEqualityNode(astBinaryOpNode):
    ' represents == and != operations '
    def __init__(self, typ, lhs, rhs, op):
        astBinaryOpNode.__init__(self, typ, lhs, rhs, op)

class astUnaryOpNode(astNode):
    def __init__(self, typ, lhs, op):
        astNode.__init__(self, 'unaOp', lhs)
        self.typ_str = typ
        self.lhs = lhs
        self.op = op

class astDefinedNode(astNode):
    def __init__(self, symbol):
        astNode.__init__(self, 'defined', symbol)

class astNotNode(astUnaryOpNode):
    def __init__(self, lhs):
        op = lambda x,symdb: not x
        astUnaryOpNode.__init__(self, '!', lhs, op)

class astAndNode(astBinaryOpNode):
    def __init__(self, lhs, rhs, op):
        astBinaryOpNode.__init__(self, '&&', lhs, rhs, op)

class astOrNode(astBinaryOpNode):
    def __init__(self, lhs, rhs, op):
        astBinaryOpNode.__init__(self, '||', lhs, rhs, op)


class ExprParser(GenericParser):
    def __init__(self, line, startToken='cond'):
        GenericParser.__init__(self, startToken)
        self.line = line

    def p_simple_cond(self, args):
        '''
            cond ::= atomic_cond
        '''
        return args[0]

    def p_negate(self, args):
        '''
            cond ::= ! atomic_cond
        '''
        return astNotNode(args[1])

    def p_and(self, args):
        '''
            cond ::= atomic_cond && atomic_cond
        '''
        return astAndNode(args[0], args[2], lambda x,y: x and y)

    def p_or(self, args):
        '''
            cond ::= atomic_cond || atomic_cond
        '''
        return astOrNode(args[0], args[2], lambda x,y: x or y)

    def p_simple_atomic_cond(self, args):
        '''
            atomic_cond ::= sum
        '''
        return args[0]

    def p_equal_atomic_cond(self, args):
        '''
            atomic_cond ::= sum == sum
        '''
        return astEqualityNode('==', args[0], args[2], lambda x,y: x==y)

    def p_unequal_atomic_cond(self, args):
        '''
            atomic_cond ::= sum != sum
        '''
        return astEqualityNode('!=', args[0], args[2], lambda x,y: x!=y)


    def p_plus(self, args):
        '''
            sum ::= product + product
        '''
        return astSumNode('+', args[0], args[2], lambda x,y: x+y)

    def p_minus(self, args):
        '''
            sum ::= product - product
        '''
        return astSumNode('-', args[0], args[2], lambda x,y: x-y)

    def p_unary_sum(self, args):
        '''
            sum ::= product
        '''
        # We transform this expression to "number + 0" and forward it to the
        # standard addition rule
        return self.p_plus([args[0], OP_PLUS, CONSTANT_ZERO])

    def p_mul(self, args):
        '''
            product ::= atom * atom
        '''
        return astProductNode('*', args[0], args[2], lambda x,y: x*y)

    def p_div(self, args):
        '''
            product ::= atom / atom
        '''
        return astProductNode('/', args[0], args[2], lambda x,y: x/y)

    def p_unary_product(self, args):
        '''
            product ::= atom
        '''
        # We transform this expression to "number * 1" and forward it to the
        # standard multiplication rule
        return self.p_mul([args[0], OP_MUL, CONSTANT_ONE])

    def p_defined(self, args):
        '''
            product ::= defined symbol
        '''
        return astDefinedNode(args[1].value)

    def p_paren_defined(self, args):
        '''
            product ::= defined ( symbol )
        '''
        return astDefinedNode(args[2].value)

    def p_atom(self, args):
        '''
            atom ::= symbol
            atom ::= number
        '''
        # This rule exists to simplify the product rules
        return args[0]

    def p_parens(self, args):
        '''
            atom ::= ( cond )
        '''
        return args[1]

    def error(self, token):
        print "line {0}: Syntax error at or near `{1}' token".format(self.line, token)
        raise SystemExit
