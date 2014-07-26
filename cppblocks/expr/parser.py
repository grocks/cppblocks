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

class astUnaryOpNode(astNode):
    def __init__(self, typ, lhs, op):
        astNode.__init__(self, 'unaOp', lhs)
        self.typ_str = typ
        self.lhs = lhs
        self.op = op

class astDefinedNode(astUnaryOpNode):
    def __init__(self, lhs):
        op = lambda x,symdb: symdb.defined(x)
        astUnaryOpNode.__init__(self, 'defined', lhs, op)

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

class astAndNode(astNode):
    def __init__(self, expr):
        astNode.__init__(self, '&&')
        self.children.append(expr)

class astOrNode(astNode):
    def __init__(self, expr):
        astNode.__init__(self, '||')
        self.children.append(expr)


class ExprParser(GenericParser):
    def __init__(self, startToken='cond'):
        GenericParser.__init__(self, startToken)

    def p_cond(self, args):
        '''
            cond ::= atomic_cond
        '''
        return args[0]

    def p_atomic_cond(self, args):
        '''
            atomic_cond ::= sum
        '''
        return args[0]

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
        return astDefinedNode(args[1])

    def p_atom(self, args):
        '''
            atom ::= symbol
            atom ::= number
        '''
        # This rule exists to simplify the product rules
        return args[0]








































#    def p_expr(self, args):
#        '''
#            expr ::= condOr
#        '''
#        return args[0]
#
#    def p_number(self, args):
#        '''
#            basicExpr ::= number
#        '''
#        t = args[0]
#        return astNode('number', t.value)
#
#    def p_symbol(self, args):
#        '''
#            basicExpr ::= symbol
#        '''
#        t = args[0]
#        return astNode('symbol', t.value)
#
#    def p_defined(self, args):
#        '''
#            basicExpr ::= defined symbol
#            basicExpr ::= defined ( symbol )
#        '''
#        if len(args) == 2:
#            t = args[1]
#        else:
#            t = args[2]
#        return astNode('defined', t.value)
#
#    def p_not(self, args):
#        '''
#            expr ::= ! expr
#        '''
#        return astNotNode(expr=args[1])
#
#    def p_parenthesizedExpression(self, args):
#        '''
#            expr ::= ( expr )
#        '''
#        return args[1]
#
#    def p_equality(self, args):
#        '''
#            equalityExpr ::= equalityExpr == equalityExpr
#            equalityExpr ::= equalityExpr != equalityExpr
#        '''
#        opType = args[1].typ
#        return astEqualityNode(lhs=args[0], op=opType, rhs=args[2])
#
#    def p_simpleEquality(self, args):
#        '''
#        equalityExpr ::= basicExpr
#        '''
#        return args[0]
#
#    def p_conditionalOr(self, args):
#        '''
#            condOr ::= condOr || condAnd
#        '''
#        condOr = args[0]
#        condAnd = args[2]
#        condOr.children.append(condAnd)
#        return condOr
#
#    def p_simpleConditionalOr(self, args):
#        '''
#            condOr ::= condAnd
#        '''
#        condAnd = args[0]
#        return astOrNode(condAnd)
#
#    def p_conditionalAnd(self, args):
#        '''
#            condAnd ::= condAnd equalityExpr
#        '''
#        condAnd = args[0]
#        equExpr = args[1]
#        condAnd.children.append(equExpr)
#        return condAnd
#
#    def p_simpleConditionalAnd(self, args):
#        '''
#            condAnd ::= equalityExpr
#        '''
#        equExpr = args[0]
#        return astAndNode(equExpr)

#   def p_logicalOR(self, args):
#       '''
#           OR_expr ::= AND_expr || AND_expr
#       '''
#       return astOrNode(lhs=args[0], rhs=args[1])

#   def p_logicalAND(self, args):
#       '''
#           AND_expr ::= expr && expr
#       '''
#       return astAndNode(lhs=args[0], rhs=args[1])

#   def p_emptyLogicalAND(self, args):
#       '''
#           AND_expr ::= expr
#       '''
#       # This Rule is required, because p_logicalOR() is built on the AND_expr
#       return args[0]

#   def p_emptyLogicalOR(self, args):
#       '''
#           OR_expr ::= AND_expr
#       '''
#       return args[0]

#   def p_logicalOrAndExpression(self, args):
#       '''
#           expr ::= OR_expr
#       '''
#       return args[0]
