'''
The CppScanner parses a C source file for CPP directives and tokenizes them.

The CppScanner is hand written and does not use the GenericScanner from Spark,
because Spark does not support the line-based syntax of CPP directives mixed
within C source code.
'''

import re

# We compile all regular expression used for parsing to speed up the tokenization process
reCppDirective = re.compile(r'^\s*\#')
reDefine = re.compile('^\s*#\s*define\s+([A-Za-z_][A-Za-z_0-9]*)(\s+(.*))?$')
reIfdef = re.compile('^\s*#\s*ifdef\s+([A-Za-z_][A-Za-z_0-9]*)$')
reIfndef = re.compile('^\s*#\s*ifndef\s+([A-Za-z_][A-Za-z_0-9]*)$')
reEndif = re.compile('^\s*#\s*endif\s*$')

# Test if the line is a CPP directive, i.e., start with a #
def isCppDirective(line):
    return reCppDirective.match(line)

class Token:
    def __init__(self, typ, line):
        self.typ = typ
        self.line = line

    def __str__(self):
        return 'line {0}: {1}'.format(self.line, self.typ)

    def __repr__(self):
        return self.__str__()

class IfDefToken(Token):
    def __init__(self, line, symbol):
        Token.__init__(self, 'ifdef', line)
        self.symbol = symbol

    def __str__(self):
        return '{0}({1})'.format(Token.__str__(self), self.symbol)

class IfnDefToken(Token):
    def __init__(self, line, symbol):
        Token.__init__(self, 'ifndef', line)
        self.symbol = symbol

    def __str__(self):
        return '{0}({1})'.format(Token.__str__(self), self.symbol)

class EndIfToken(Token):
    def __init__(self, line):
        Token.__init__(self, 'endif', line)

class DefineToken(Token):
    def __init__(self, line, name, value):
        Token.__init__(self, 'define', line)
        self.name = name
        self.value = value

    def __str__(self):
        return '{0}({1}={2})'.format(Token.__str__(self), self.name, self.value)

class CppScanner:
    def __init__(self, data):
        self.rv = []
        self.lines = data.splitlines()
        self.currentLine = 0
        # TODO: Add multi-line handling at this point

    def tokenize(self):
        for line in self.lines:
            self.currentLine += 1
            self.tokenizeLine(line)

        return self.rv

    def tokenizeLine(self, line):
        # Skip line if it is not a CPP directive
        if not isCppDirective(line):
            return

        # Check for a #define
        match = reDefine.match(line)
        if match:
            self.t_define(match)

        # Check for a #ifdef
        match = reIfdef.match(line)
        if match:
            self.t_ifdef(match)

        # Check for a #ifndef
        match = reIfndef.match(line)
        if match:
            self.t_ifndef(match)

        # Check for a #endif
        match = reEndif.match(line)
        if match:
            self.t_endif(match)

    def t_ifdef(self, m):
        t = IfDefToken(self.currentLine, symbol=m.group(1))
        self.rv.append(t)

    def t_ifndef(self, m):
        t = IfnDefToken(self.currentLine, symbol=m.group(1))
        self.rv.append(t)

    def t_endif(self, m):
        self.rv.append(EndIfToken(self.currentLine))

    def t_define(self, m):
        # Remember: m.group(2) includes the space separating name and value in
        #               #define NAME<space>VALUE
        t = DefineToken(self.currentLine, name=m.group(1), value=m.group(3))
        self.rv.append(t)