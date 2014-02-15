'''
getDisabledBlocks
'''

from checkargs import check as checkArgs
from predefines import importPredefinedSymbols
from database import Database
from fileparser import CppFileParser

from scanner import CppScanner
from parser import CppParser
from compiler import DisabledBlocksCompiler

def getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines):
    checkargs.check(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)

    database = Database()

    importPredefinedSymbols(database, initialDefines)

    with open(filepath, 'r') as f:
        data = f.read()

    scanner = CppScanner(data)
    tokens = scanner.tokenize()

    parser = CppParser()
    astRootNode = parser.parse(tokens)

    disabledBlocks = []
    compiler = DisabledBlocksCompiler(filepath, database, astRootNode)
    disabledBlocks = compiler.getDisabledBlocks()

    return disabledBlocks
