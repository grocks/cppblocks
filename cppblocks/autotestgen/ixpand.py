''' Include expansion tool

This library expands include directives (recursively) in a C source code file.

Summary: lines with a #include directive are replaced with the included file.
'''

import md5
import sys

from cleaner import stripComments, joinMultiLines
from scanner import reIncludeAngle, reIncludeQuote, reCppDirective
from messages import FileNotFound

class FileHistoryCache:
    ''' Caches already visited files. '''

    def __init__(self):
        self.cache = {}

    def update(self, filepath):
        ''' Add a file to the cache.

        Returns True if the file is original and False if its already in the cache.
        '''
        try:
            with open(filepath, 'r') as f:
                checksum = md5.md5(f.read()).hexdigest()
                if self.cache.has_key(checksum):
                    return False
                else:
                    self.cache[checksum] = True
                    return True
        except IOError as e:
            print >> sys.stderr, 'Warning: failed to compute md5sum for {0}! Reason: {1}'.format(filepath, e)
            return True # Assume an original file in this case

def expandIncludes(filepath, fileFinderAngleInclude, fileFinderQuoteInclude, fileHistoryCache=None):
    ''' Expand all #includes in the given file and return expanded content.

    This function works recursively via getIncludedTextBlocks().
    '''
    # Create the file history cache for the top-level invocation. The recursive
    # values will pass this instance down the call chain.
    if not fileHistoryCache:
        fileHistoryCache = FileHistoryCache()

    # Do not visit a file twice (=> break recursion / handle include guards)
    if not fileHistoryCache.update(filepath):
        return '/* File "{0}" already visited! */'.format(filepath)

    with open(filepath, 'r') as f:
        fileContent = f.read()

    fileContent = stripComments(fileContent)
    lines = fileContent.split('\n')

    cleanedLines = joinMultiLines(lines)

    includedTextBlocks = getIncludedTextBlocks(filepath, cleanedLines, fileFinderAngleInclude, fileFinderQuoteInclude, fileHistoryCache)

    for textBlock in includedTextBlocks:
        lines[textBlock['lineIdx']] = textBlock['text']

    return "\n".join(lines)

def getIncludedTextBlocks(filepath, lines, fileFinderAngleInclude, fileFinderQuoteInclude, fileHistoryCache):
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
                textBlock = expandIncludes(incFilePath, fileFinderAngleInclude, fileFinderQuoteInclude, fileHistoryCache)
                textBlocks.append({ 'lineIdx': idx, 'text': textBlock })

        except FileNotFound as e:
            errorMessage = '#error "{0}"'.format(e.message)
            textBlocks.append({ 'lineIdx': idx, 'text': errorMessage })

    return textBlocks
