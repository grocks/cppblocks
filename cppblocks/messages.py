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

class InternalError(CppBlocksException):
    def __init__(self, error):
        self.message = "An internal error occurred. Description: {0}".format(error)

class LexicalError(CppBlocksException):
    def __init__(self, filepath, line, column, expression):
        self.filepath = filepath
        self.line = line
        self.column = column
        self.expression = expression
        self.message = "{0}:{1}: lexical error at position {2}\n{3}\n{4}".format(
                self.filepath,
                self.line,
                self.column,
                self.expression,
                ' '*(self.column-1) + '^'
        )
