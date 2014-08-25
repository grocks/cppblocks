''' Include expansion tool

This library expands include directives (recursively) in a C source code file.

Summary: lines with a #include directive are replaced with the included file.
'''

from cleaner import stripComments, joinMultiLines
from scanner import reIncludeAngle, reIncludeQuote
from messages import FileNotFound

def expandIncludes(filepath, fileFinderAngleInclude, fileFinderQuoteInclude):
    ''' Expand all #includes in the given file and return expanded content.

    This function works recursively via getIncludedTextBlocks().
    '''
    with open(filepath, 'r') as f:
        fileContent = f.read()

    fileContent = stripComments(fileContent)
    lines = fileContent.split('\n')

    cleanedLines = joinMultiLines(lines)

    includedTextBlocks = getIncludedTextBlocks(filepath, cleanedLines, fileFinderAngleInclude, fileFinderQuoteInclude)

    for textBlock in includedTextBlocks:
        lines[textBlock['lineIdx']] = textBlock['text']

    return "\n".join(lines)

def getIncludedTextBlocks(filepath, lines, fileFinderAngleInclude, fileFinderQuoteInclude):
    ''' Return content of all included header files.

    This function works recursively via expandIncludes().
    '''
    textBlocks = []

    for idx in xrange(len(lines)):
        line = lines[idx]

        try:
            incFilePath = None
            match = reIncludeAngle.match(line)
            if match:
                incFilePath = fileFinderAngleInclude.lookup(match.group(1))
            else:
                match = reIncludeQuote.match(line)
                if match:
                    incFilePath = fileFinderQuoteInclude.lookup(filepath, match.group(1))

            if match:
                textBlock = expandIncludes(incFilePath, fileFinderAngleInclude, fileFinderQuoteInclude)
                textBlocks.append({ 'lineIdx': idx, 'text': textBlock })

        except FileNotFound as e:
            errorMessage = '#error "{0}"'.format(e.message)
            textBlocks.append({ 'lineIdx': idx, 'text': errorMessage })

    return textBlocks
