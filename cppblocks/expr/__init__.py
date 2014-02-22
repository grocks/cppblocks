'''
    The 'expr' module contains a scanner, parser and interpreter of #if/#elif
    conditional expressions.
'''

def evalCondExpression(database, expression):
    if expression.isdigit():
        expr = expression
    else:
        expr = database.getValue(expression)

    return int(expr)
