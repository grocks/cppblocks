'''
Diagnostic (error) messages are defined in this file as Python exceptions.
'''

class CppBlocksException(Exception):
    '''Base class for CppBlocks exceptions.'''
    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()

class UndefinedSymbol(CppBlocksException):
    def __init__(self, name):
        self.message = "Undefined symbol '{0}' encountered.".format(name)

class IllegalSymbol(CppBlocksException):
    def __init__(self, name):
        self.message = "The token '{0}' does not form a valid CPP symbol.".format(name)

class FileNotFound(CppBlocksException):
    def __init__(self, filepath):
        self.message = "Could not locate file '{0}'.".format(filepath)

class UnsupportedToken(CppBlocksException):
    def __init__(self, token):
        self.message = "Parser does not support handling of '{0}'".format(token)
