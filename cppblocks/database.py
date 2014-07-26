'''
A symbol database for CPP tokens/symbols defined with #define
'''

from messages import IllegalSymbol,UndefinedSymbol
import re

class Database:
    def __init__(self):
        self.symbols = {}

    def add(self, symbol, value=None):
        Database.validate(symbol)
        self.symbols[symbol] = value

    def remove(self, symbol):
        del self.symbols[symbol]

    def defined(self, symbol):
        return symbol in self.symbols

    def getValue(self, symbol, recursive=True):
        '''Return the fully expanded value of a symbol.

        Lookup the value of 'symbol'. Perform recursive lookups if the symbol is mapped to another symbol.
        '''
        if not self.defined(symbol):
            # Undefined symbols evaluate to zero according to the C standard
            return 0
        else:
            value = self.symbols[symbol]

            # Symbols without a defined value evalute to zero
            if value is None:
                return 0

            # Test if the symbol evaluates to a numberic value or to another symbol
            if len(value) and value[0].isdigit():
                return value
            elif len(value) and recursive:
                return self.getValue(value, recursive)
            else:
                # Symbols with 'empty' value are handled in this case (return value is the empty string '')
                return self.symbols[symbol]

    @staticmethod
    def isValidCppToken(token):
        '''This function checks if the given token is a valid CPP symbol.'''
        return re.search('^[A-Za-z_]([A-Za-z_0-9]*)$', token)

    @staticmethod
    def validate(token):
        if not Database.isValidCppToken(token):
            raise IllegalSymbol(token)
