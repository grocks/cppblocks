'''
A parser for C source files on a preprocessing level
'''

from database import Database
from messages import FileNotFound
import re

class CppParser:
    def __init__(self, filepath, database):
        self.filepath = filepath
        self.symbols = database

        # Compile some regular expressions for efficiency
        self.reDefine = re.compile('^\s*#\s*define\s+([A-Za-z_][A-Za-z_0-9]*)(\s+(.*))?$')
        self.reIfdef = re.compile('^\s*#\s*if(n)?def\s+([A-Za-z_][A-Za-z_0-9]*)$')
        self.reEndif = re.compile('^\s*#\s*endif\s*$')

        # Set if we are in disabled conditional block
        self.skipBlock = False
        self.startOfBlock = None
        self.currentLine = 0

        # List of disabled blocks, we encountered in this file
        self.disabledBlocks = []

        # Read file content into memory
        with file(filepath) as f:
            self.content = f.readlines()

    def parse(self):
        for line in self.content:
            self.currentLine += 1
            self.parseLine(line)

        return [ { 'filepath' : self.filepath,
                   'disabledBlocks' : self.disabledBlocks } ]

    def parseLine(self, line):
        if not self.skipBlock:
            # Check for a #define
            match = self.reDefine.search(line)
            if match:
                self.parseDefine(match)

            # Check for a #ifdef
            match = self.reIfdef.search(line)
            if match:
                self.parseIfdef(match)
        else:
            match = self.reEndif.search(line)
            if match:
                self.parseEndif(match)

    def parseDefine(self, match):
        symbol = match.group(1)
        value = match.group(3) or None
        self.symbols.add(symbol, value)

    def parseIfdef(self, match):
        negated = match.group(1)
        symbol = match.group(2)

        defined = self.symbols.defined(symbol)

        # Mark if condition is false
        if (not negated and not defined) or (negated and defined):
            self.skipBlock = True
            self.startOfBlock = self.currentLine

    def parseEndif(self, match):
        length = self.currentLine - self.startOfBlock + 1
        self.addDisabledBlock(self.startOfBlock, length)
        self.skipBlock = False

    def addDisabledBlock(self, start, length):
        self.disabledBlocks.append( (start,length) )
