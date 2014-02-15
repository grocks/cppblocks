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

class astIfdefNode(astNode):
    def __init__(self, line, symbol):
        astNode.__init__(self, 'ifdef', line)
        self.symbol = symbol
        self.length = line

class astIfndefNode(astNode):
    def __init__(self, line, symbol):
        astNode.__init__(self, 'ifndef', line)
        self.symbol = symbol
        self.length = line

class astEndifNode(astNode):
    def __init__(self, line):
        astNode.__init__(self, 'endif', line)


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
            ifSection ::= ifGroup group endif
        '''
        # Can also be an ifndef node
        astIfdefNode = args[0]
        endifToken = args[2]
        astIfdefNode.length = endifToken.line - astIfdefNode.line + 1
        astIfdefNode.children.append(args[1])
        return astIfdefNode

    def p_leafIfSection(self, args):
        '''
            ifSection ::= ifGroup endif
        '''
        # Can also be an ifndef node
        astIfdefNode = args[0]
        endifToken = args[1]
        astIfdefNode.length = endifToken.line - astIfdefNode.line + 1
        return astIfdefNode

    def p_ifdef(self, args):
        '''
            ifGroup ::= ifdef
        '''
        t = args[0]
        return astIfdefNode(t.line, t.symbol)

    def p_ifndef(self, args):
        '''
            ifGroup ::= ifndef
        '''
        t = args[0]
        return astIfndefNode(t.line, t.symbol)

    def p_define(self, args):
        '''
            controlLine ::= define
        '''
        t = args[0]
        return astDefineNode(t.line, t.name, t.value)
