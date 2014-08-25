''' The code mangler strips a source file of all non-preprocessing directives.

The code mangler replaces all lines in a source files that do not contain a
preprocessing directive with the current line number.

Such a translated file can be used by the automatic test generator.
'''

from cleaner import stripComments, joinMultiLines
from scanner import reCppDirective

def replaceNonCppLinesWithLineNumbers(fileContent):
    fileContent = stripComments(fileContent)
    lines = fileContent.split('\n')

    cleanedLines = joinMultiLines(lines)

    for idx in xrange(len(cleanedLines)):
        line = cleanedLines[idx]

        # Pass multi-line lines (i.e., leave multi-line preprocessing directive intact)
        if line.endswith('\\'):
            continue

        if not reCppDirective.match(line):
            lines[idx] = idx+1

    # Compress the file, by replacing adjacent lines with line numbers
    lines = collapseAdjacentNumbers(lines)

    # Get a list of all numbered lines (i.e., non CPP lines)
    nonCppLineNumberList = filter(lambda elt: isinstance(elt,int), lines)

    # Replace the line numbers of type 'int' with strings (necessary for str.join)
    lines = map(str, lines)

    return { 'nonCppLineNumberList': nonCppLineNumberList, 'text': "\n".join(lines) }

def collapseAdjacentNumbers(array):
    ''' Replace multiple 'int' elements in the array with idx+1 of first 'int' element. '''

    condensedArray = []
    nextLine = 1

    skipInts = False

    for idx in xrange(len(array)):
        elt = array[idx]

        # Skip adjacent integers
        if type(elt) is int and skipInts:
            continue
        # Found the first integer after a non-integer element?
        elif type(elt) is int:
            skipInts = True
            condensedArray.append(nextLine)
        # Found a non-integer? Copy it to condensedArray
        elif not type(elt) is int:
            skipInts = False
            condensedArray.append(elt)

        # Increase line counter for the condensed array
        nextLine += 1

    return condensedArray
