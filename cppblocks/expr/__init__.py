'''
    The 'expr' module contains a scanner, parser and interpreter of #if/#elif
    conditional expressions.
'''

from scanner import ExprScanner
from parser import ExprParser
from interpreter import ExprInterpreter

def evalCondExpression(database, expression, line):
    scanner = ExprScanner()
    tokens = None
    try:
        tokens = scanner.tokenize(expression)
    except SystemExit as e:
        print "Error in line '{0}'".format(line)
        print "Exception: {0}".format(e)

    parser = ExprParser(line)
    rootNode = parser.parse(tokens)

    interpreter = ExprInterpreter(database)
    res =  interpreter.evaluate(rootNode)

    #print "'{0}' -> {1}".format(expression, res)

    return res
