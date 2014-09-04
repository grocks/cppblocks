'''
    The 'expr' module contains a scanner, parser and interpreter of #if/#elif
    conditional expressions.
'''

import trace
def log(*args):
    trace.trace('cppblocks.expr.eval', *args)

from scanner import ExprScanner
from parser import ExprParser
from interpreter import ExprInterpreter
from ..messages import LexicalError

def evalCondExpression(database, expression, filepath, line):
    scanner = ExprScanner(filepath, line)
    tokens = scanner.tokenize(expression)

    parser = ExprParser(line)
    rootNode = parser.parse(tokens)

    interpreter = ExprInterpreter(database)
    res =  interpreter.evaluate(rootNode)

    return res
