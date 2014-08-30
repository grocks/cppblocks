''' The code mangler strips a source file of all non-preprocessing directives.

In the second step, the code mangler marks all CPP conditional blocks by line
number markers. Thus, each block created by #if, #ifdef, #ifndef, #elif, #else
and #endif is marked by a pair of line numbers.

Such a translated file can be used by the automatic test generator.
'''

import re

from cleaner import stripComments, joinMultiLines

from scanner import reCppDirective, reIf, reIfdef, reIfndef, reElif, reElse, reEndif

def stripNonCppDirectives(fileContent):
    ''' Removes all non-cpp directive lines from the given source code. '''
    fileContent = stripComments(fileContent)
    lines = fileContent.split('\n')

    lines = joinMultiLines(lines)

    for idx in xrange(len(lines)):
        line = lines[idx]

        # Pass multi-line lines (i.e., leave multi-line preprocessing directive intact)
        if line.endswith('\\'):
            continue

        if not reCppDirective.match(line):
            lines[idx] = ''

    return collapseEmptyLines(lines)

def markConditionalBlocks(lines):
    ''' Mark all CPP directives that are involved in branching with line numbers. '''
    markedLines = []
    nextLine = 1

    for line in lines:
        if reIf.match(line) or reIfdef.match(line) or reIfndef.match(line):
            # Line number of #if follows on the next line
            markedLines.append(line)
            markedLines.append(nextLine)
            nextLine += 2
        elif reElif.match(line) or reElse.match(line):
            # Current line number preceeds #elif/#else
            markedLines.append(nextLine)
            markedLines.append(line)
            # Line number of #elif/#else follows on the next line
            nextLine += 1
            markedLines.append(nextLine)
            nextLine += 1
        elif reEndif.match(line):
            # Current line number preceeds #endif
            markedLines.append(nextLine)
            markedLines.append(line)
            nextLine += 2
        else:
            # All the other lines are simply forwarded to the output array
            markedLines.append(line)
            nextLine += 1

    # Get a list of all markers (lines numbers following/preceeding the CPP directives)
    cppBlockMarkerList = filter(lambda elt: isinstance(elt,int), markedLines)

    # Replace the line numbers of type 'int' with strings (necessary for str.join)
    markedLines = map(str, markedLines)

    return { 'cppBlockMarkerList': cppBlockMarkerList, 'text': "\n".join(markedLines) }

def collapseEmptyLines(array):
    ''' Removes empty lines from the array. '''

    return filter(len, array)
