'''
A parser for C source files on a preprocessing level
'''

from database import Database

class CppParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.symbols = Database()
