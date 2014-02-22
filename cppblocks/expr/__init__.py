'''
    The 'expr' module contains a scanner, parser and interpreter of #if/#elif
    conditional expressions.
'''

from scanner import ExprScanner
from parser import ExprParser
from interpreter import ExprInterpreter

def evalCondExpression(database, expression):
    scanner = ExprScanner()
    tokens = scanner.tokenize(expression)

    parser = ExprParser()
    rootNode = parser.parse(tokens)

    interpreter = ExprInterpreter(database)
    return interpreter.evaluate(rootNode)

    if expression.isdigit():
        expr = expression
    else:
        expr = database.getValue(expression)

    return int(expr)
