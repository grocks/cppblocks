'''
A high-level function that invokes the scanner, parser and compiler.
'''

from scanner import CppScanner
from parser import CppParser
from compiler import DisabledBlocksCompiler
from cleaner import stripComments

def analyzeFile(filepath, analyzeHeaders, fileFinderAngleInclude, fileFinderQuoteInclude, symbolDatabase):
    with open(filepath, 'r') as f:
        fileContent = f.read()

    fileContent = stripComments(fileContent)

    scanner = CppScanner(fileContent)
    tokens = scanner.tokenize()

    parser = CppParser()
    astRootNode = parser.parse(tokens)

    disabledBlocks = []
    compiler = DisabledBlocksCompiler(filepath, analyzeHeaders, symbolDatabase, fileFinderAngleInclude, fileFinderQuoteInclude, astRootNode)
    disabledBlocks = compiler.getDisabledBlocks()

    return disabledBlocks

