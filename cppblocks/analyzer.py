'''
A high-level function that invokes the scanner, parser and compiler.
'''

import trace
def log(*args):
    trace.trace('cppblocks.analyzer', *args)

from scanner import CppScanner
from parser import CppParser
from compiler import DisabledBlocksCompiler
from cleaner import stripComments, joinMultiLines


def analyzeFile(filepath, analyzeHeaders, fileFinderAngleInclude, fileFinderQuoteInclude, symbolDatabase):

    log('analyzing ' + filepath)

    with open(filepath, 'r') as f:
        fileContent = f.read()

    fileContent = stripComments(fileContent)

    lines = fileContent.splitlines()
    lines = joinMultiLines(lines)

    scanner = CppScanner(lines)
    tokens = scanner.tokenize()

    log('tokens', "\n".join(map(str,tokens)))

    parser = CppParser()
    astRootNode = parser.parse(tokens)

    log('ast', astRootNode)

    disabledBlocks = []
    compiler = DisabledBlocksCompiler(filepath, analyzeHeaders, symbolDatabase, fileFinderAngleInclude, fileFinderQuoteInclude, astRootNode)
    disabledBlocks = compiler.getDisabledBlocks()

    return disabledBlocks

