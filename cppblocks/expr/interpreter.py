'''
An interpreter for #if/#elif conditional expressions.

The interpreter evaluates the conditional expression and returns its truth value.
'''

class ExprInterpreter:
    def __init__(self, symdb):
        self.symdb = symdb

        self.visitorMap = {
                'symbol' : self.v_symbol,
                'number' : self.v_number
        }

    def evaluate(self, rootNode):
        visitor = self.visitorMap[rootNode.typ]
        return visitor(rootNode)

    def v_symbol(self, node):
        return int(self.symdb.getValue(node.value))

    def v_number(self, node):
        return int(node.value)
