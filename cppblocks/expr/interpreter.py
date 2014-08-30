'''
An interpreter for #if/#elif conditional expressions.

The interpreter evaluates the conditional expression and returns its truth value.
'''

import re

def toInt(numAsStr):
    'Convert a C-style number literal to a Python integer.'
    if (not type(numAsStr) is str):
        return numAsStr # Forward everything that is not a string (re.sub requires a string)
    # Remove the trailing literal modifiers, e.g., "u", "ul", "s"
    s = re.sub(r'[a-zA-Z]*$', '', numAsStr)
    return int(s) # Convert to int


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
        return toInt(self.symdb.getValue(node.value))

    def v_number(self, node):
        return toInt(node.value)

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
