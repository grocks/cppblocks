'''
An importer function for predefined CPP symbols.


This functions is not yet that useful. Its usefulness begins once CppBlocks
supports CPP macros.
'''

def importPredefinedSymbols(database, symbols):
    for symbol in symbols.keys():
        database.add(symbol, symbols[symbol])
