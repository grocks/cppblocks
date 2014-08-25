'''
The CppScanner parses a C source file for CPP directives and tokenizes them.

The CppScanner is hand written and does not use the GenericScanner from Spark,
because Spark does not support the line-based syntax of CPP directives mixed
within C source code.
'''

import re

# We compile all regular expression used for parsing to speed up the tokenization process
reCppDirective = re.compile(r'^\s*\#')
reDefine = re.compile('^\s*#\s*define\s+([A-Za-z_][A-Za-z_0-9]*)(\s+(.*))?\s*$')
reUndef = re.compile('^\s*#\s*undef\s+([A-Za-z_][A-Za-z_0-9]*)\s*$')
reIfdef = re.compile('^\s*#\s*ifdef\s+([A-Za-z_][A-Za-z_0-9]*)\s*$')
reIfndef = re.compile('^\s*#\s*ifndef\s+([A-Za-z_][A-Za-z_0-9]*)\s*$')
reIf = re.compile('^\s*#\s*if\s+(.*)\s*$')
reElif = re.compile('^\s*#\s*elif\s+(.*)\s*$')
reElse = re.compile('^\s*#\s*else\s*$')
reEndif = re.compile('^\s*#\s*endif\s*$')
reIncludeAngle = re.compile('^\s*#\s*include\s*<([^>]+)>\s*$')
reIncludeQuote = re.compile('^\s*#\s*include\s*"([^"]+)"\s*$')

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

    def __cmp__(self, o):
        return cmp(self.typ, o)

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

class IfToken(Token):
    def __init__(self, line, expression):
        Token.__init__(self, 'if', line)
        self.expression = expression

    def __str__(self):
        return '{0}({1})'.format(Token.__str__(self), self.expression)

class ElifToken(Token):
    def __init__(self, line, expression):
        Token.__init__(self, 'elif', line)
        self.expression = expression

    def __str__(self):
        return '{0}({1})'.format(Token.__str__(self), self.expression)

class ElseToken(Token):
    def __init__(self, line):
        Token.__init__(self, 'else', line)

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

class UndefToken(Token):
    def __init__(self, line, symbol):
        Token.__init__(self, 'undef', line)
        self.symbol = symbol

    def __str__(self):
        return '{0}({1})'.format(Token.__str__(self), self.symbol)

class IncludeAngleToken(Token):
    def __init__(self, line, path):
        Token.__init__(self, 'includeAngle', line)
        self.path = path

    def __str__(self):
        return '{0}({1})'.format(Token.__str__(self), self.path)

class IncludeQuoteToken(Token):
    def __init__(self, line, path):
        Token.__init__(self, 'includeQuote', line)
        self.path = path

    def __str__(self):
        return '{0}({1})'.format(Token.__str__(self), self.path)

class CppScanner:
    ''' This scanner requires some pre-processing on its input.

    Backslash-escaped lines (multi-line directives) must be joined into a
    single line and comments must be stripped from the file.

    Additionally, the number of lines in the file must not be altered, or the
    output of CppBlocks won't match the given input file anymore.

    This preprocessing is done in analyzeFile() from analyzer.py
    '''
    def __init__(self, lines):
        self.rv = []
        self.lines = lines
        self.currentLine = 0

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

        # Check for a #undef
        match = reUndef.match(line)
        if match:
            self.t_undef(match)

        # Check for a #ifdef
        match = reIfdef.match(line)
        if match:
            self.t_ifdef(match)

        # Check for a #ifndef
        match = reIfndef.match(line)
        if match:
            self.t_ifndef(match)

        # Check for a #if
        match = reIf.match(line)
        if match:
            self.t_if(match)

        # Check for a #elif
        match = reElif.match(line)
        if match:
            self.t_elif(match)

        # Check for a #else
        match = reElse.match(line)
        if match:
            self.t_else(match)

        # Check for a #endif
        match = reEndif.match(line)
        if match:
            self.t_endif(match)

        # Check for a #include <>
        match = reIncludeAngle.match(line)
        if match:
            self.t_includeAngle(match)

        # Check for a #include ""
        match = reIncludeQuote.match(line)
        if match:
            self.t_includeQuote(match)

    def t_ifdef(self, m):
        t = IfDefToken(self.currentLine, symbol=m.group(1))
        self.rv.append(t)

    def t_ifndef(self, m):
        t = IfnDefToken(self.currentLine, symbol=m.group(1))
        self.rv.append(t)

    def t_if(self, m):
        t = IfToken(self.currentLine, expression=m.group(1))
        self.rv.append(t)

    def t_elif(self, m):
        t = ElifToken(self.currentLine, expression=m.group(1))
        self.rv.append(t)

    def t_else(self, m):
        t = ElseToken(self.currentLine)
        self.rv.append(t)

    def t_endif(self, m):
        self.rv.append(EndIfToken(self.currentLine))

    def t_define(self, m):
        # Remember: m.group(2) includes the space separating name and value in
        #               #define NAME<space>VALUE
        t = DefineToken(self.currentLine, name=m.group(1), value=m.group(3))
        self.rv.append(t)

    def t_undef(self, m):
        t = UndefToken(self.currentLine, symbol=m.group(1))
        self.rv.append(t)

    def t_includeAngle(self, m):
        t = IncludeAngleToken(self.currentLine, path=m.group(1))
        self.rv.append(t)

    def t_includeQuote(self, m):
        t = IncludeQuoteToken(self.currentLine, path=m.group(1))
        self.rv.append(t)
