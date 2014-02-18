'''
A parser for CPP directives.

The parser is implemented using the Spark GenericParser parser generator.

The token names used in the parser's grammar are taken from the C standard.
'''

from lib.spark import GenericParser

class astNode:
    def __init__(self, typ, line):
        self.typ = typ
        self.line = line
        self.children = []
        self.siblings = []

    def __str__(self,indent=0):
        str = "{0}{1}.{2}".format(indent*'  ', self.typ, self.line)
        for child in self.children:
            str = '{0}\n{1}'.format(str, child.__str__(indent+1))
        for sibling in self.siblings:
            str = '{0}\n{1}'.format(str, sibling.__str__(indent))
        return str

    def __repr__(self):
        return self.__str__()

class astDefineNode(astNode):
    def __init__(self, line, name, value):
        astNode.__init__(self, 'define', line)
        self.name = name
        self.value = value

class astUndefNode(astNode):
    def __init__(self, line, symbol):
        astNode.__init__(self, 'undef', line)
        self.symbol = symbol

class astIfdefNode(astNode):
    def __init__(self, line, symbol):
        astNode.__init__(self, 'ifdef', line)
        self.symbol = symbol
        self.length = 0

class astIfndefNode(astNode):
    def __init__(self, line, symbol):
        astNode.__init__(self, 'ifndef', line)
        self.symbol = symbol
        self.length = 0

class astIfNode(astNode):
    def __init__(self, line, expression):
        astNode.__init__(self, 'if', line)
        self.expression = expression
        self.length = 0

class astEndifNode(astNode):
    def __init__(self, line):
        astNode.__init__(self, 'endif', line)

class astIncludeAngleNode(astNode):
    def __init__(self, line, path):
        astNode.__init__(self, 'includeAngle', line)
        self.path = path


class astIncludeQuoteNode(astNode):
    def __init__(self, line, path):
        astNode.__init__(self, 'includeQuote', line)
        self.path = path

class CppParser(GenericParser):
    def __init__(self, startToken='preprocessingFile'):
        GenericParser.__init__(self, startToken)

    def p_empyPreprocessingFile(self, args):
        '''
            preprocessingFile ::=
        '''
        return None

    def p_preprocessingFile(self, args):
        '''
            preprocessingFile ::= group
        '''
        return args[0]

    def p_multiGroup(self, args):
        '''
            group ::= group groupPart
        '''
        args[0].siblings.append(args[1])
        return args[0]


    def p_singleGroup(self, args):
        '''
            group ::= groupPart
        '''
        return args[0]

    def p_groupPart(self, args):
        '''
            groupPart ::= ifSection
            groupPart ::= controlLine
        '''
        return args[0]

    def p_nestedIfSection(self, args):
        '''
            ifSection ::= ifGroup endif
        '''
        ifGroupNode = args[0]
        endifToken = args[1]
        ifGroupNode.length = endifToken.line - ifGroupNode.line + 1
        return ifGroupNode

    def p_ifdef(self, args):
        '''
            ifGroup ::= ifdef group
            ifGroup ::= ifdef
        '''
        t = args[0]
        ifdefNode = astIfdefNode(t.line, t.symbol)
        if len(args) == 2:
            ifdefNode.children.append(args[1])
        return ifdefNode

    def p_ifndef(self, args):
        '''
            ifGroup ::= ifndef group
            ifGroup ::= ifndef
        '''
        t = args[0]
        ifndefNode = astIfndefNode(t.line, t.symbol)
        if len(args) == 2:
            ifndefNode.children.append(args[1])
        return ifndefNode

    def p_if(self, args):
        '''
            ifGroup ::= if group
            ifGroup ::= if
        '''
        t = args[0]
        ifNode = astIfNode(t.line, t.expression)
        if len(args) == 2:
            ifNode.children.append(args[1])
        return ifNode

    def p_define(self, args):
        '''
            controlLine ::= define
        '''
        t = args[0]
        return astDefineNode(t.line, t.name, t.value)

    def p_undef(self, args):
        '''
            controlLine ::= undef
        '''
        t = args[0]
        return astUndefNode(t.line, t.symbol)

    def p_includeAngle(self, args):
        '''
            controlLine ::= includeAngle
        '''
        t = args[0]
        return astIncludeAngleNode(self, t.path)

    def p_includeQuote(self, args):
        '''
            controlLine ::= includeQuote
        '''
        t = args[0]
        return astIncludeQuoteNode(self, t.path)
