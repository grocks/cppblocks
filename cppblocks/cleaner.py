import re

# The regex to match C-style block comments requires the DOTALL in order to
# span multiple new lines for its matching. To handle several block comments
# after each other, the matching must be non-greedy. Hence, the .*? matching
# pattern.
reBlockComment = re.compile('/\*.*?\*/', re.DOTALL)
# The regex to match the C++-style block comments requires the MULTILINE in
# order to match every line with a C++-style comment in the string.
reLineComment = re.compile('//.*$', re.MULTILINE)

def stripComments(string):
    '''
        Replace C/C++ comments in a string with spaces and preserves new-lines
        in multi-line block comments.
    '''
    string = reBlockComment.sub(lambda m: re.sub('[^\n]', ' ', m.group(0)), string)
    string = reLineComment.sub(lambda m: re.sub('[^\n]', ' ', m.group(0)), string)
    return string
