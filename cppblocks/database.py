'''
A symbol database for CPP tokens/symbols defined with #define
'''

from messages import IllegalSymbol,UndefinedSymbol
import re

class Database:
    def __init__(self):
        self.symbols = {}

    def add(self, symbol, value=0):
        Database.validate(symbol)
        self.symbols[symbol] = value

    def defined(self, symbol):
        return symbol in self.symbols

    def getValue(self, symbol, implicit=False):
        '''Return value of a symbol.

        Provides the possibility to implicitly create not-existing symbols.
        '''
        if not self.defined(symbol):
            if not implicit:
                raise UndefinedSymbol(symbol)
            else:
                self.add(symbol)
        return self.symbols[symbol]

    @staticmethod
    def isValidCppToken(token):
        '''This function checks if the given token is a valid CPP symbol.'''
        return re.search('^[A-Za-z_]([A-Za-z_0-9]*)$', token)

    @staticmethod
    def validate(token):
        if not Database.isValidCppToken(token):
            raise IllegalSymbol(token)
