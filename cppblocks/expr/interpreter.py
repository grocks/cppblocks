'''
An interpreter for #if/#elif conditional expressions.

The interpreter evaluates the conditional expression and returns its truth value.
'''

class ExprInterpreter:
    def __init__(self, symdb):
        self.symdb = symdb

        self.visitorMap = {
                'symbol' : self.v_symbol,
                'number' : self.v_number,
                'defined' : self.v_defined,
                'binOp' : self.v_binOp,
                'unaOp' : self.v_unaOp
        }

    def evaluate(self, rootNode):
        visitor = self.visitorMap[rootNode.typ]
        return visitor(rootNode)

    def v_symbol(self, node):
        return int(self.symdb.getValue(node.value))

    def v_number(self, node):
        return int(node.value)

    def v_defined(self, node):
        return self.symdb.defined(node.value)

    def v_equality(self, node):
        lhs = self.evaluate(node.lhs)
        rhs = self.evaluate(node.rhs)
        return lhs == rhs

    def v_inequality(self, node):
        return not self.v_equality(node)

    def v_binOp(self, node):
        lhs = self.evaluate(node.lhs)
        rhs = self.evaluate(node.rhs)
        return node.op(lhs, rhs)

    def v_unaOp(self, node):
        value = self.evaluate(node.value)
        return node.op(value, self.symdb)
