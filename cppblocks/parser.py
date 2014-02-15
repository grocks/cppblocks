'''
A parser for CPP directives.

The parser is implemented using the Spark GenericParser parser generator.

The token names used in the parser's grammar are taken from the C standard.
'''

from messages import UnsupportedToken

class CppParser:
    def __init__(self, filepath, database):
        self.filepath = filepath
        self.symbols = database
        self.reset()

    def reset(self):
        self.disabledBlocks = []
        self.skipBlock = False
        self.startOfBlock = None

    def parse(self, tokens):
        self.reset()
        for token in tokens:
            if token.typ == 'define':
                self.p_define(token)
            elif token.typ == 'ifdef':
                self.p_ifdef(token)
            elif token.typ == 'ifndef':
                self.p_ifndef(token)
            elif token.typ == 'endif':
               self.p_endif(token)
            else:
                raise UnsupportedToken(token)

        return [ { 'filepath' : self.filepath,
                   'disabledBlocks' : self.disabledBlocks } ]

    def p_endif(self, token):
        if self.skipBlock == True:
            length = token.line - self.startOfBlock + 1
            self.addDisabledBlock(self.startOfBlock, length)
            self.skipBlock = False

    def p_ifdef(self, token):
        if not self.symbols.defined(token.symbol):
            self.skipBlock = True
            self.startOfBlock = token.line

    def p_ifndef(self, token):
        if self.symbols.defined(token.symbol):
            self.skipBlock = True
            self.startOfBlock = token.line

    def p_define(self, token):
        self.symbols.add(token.name, token.value)

    def addDisabledBlock(self, start, length):
        self.disabledBlocks.append( (start,length) )
