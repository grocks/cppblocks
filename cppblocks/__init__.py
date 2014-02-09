'''
getDisabledBlocks
'''

from checkargs import check as checkArgs
from predefines import importPredefinedSymbols
from database import Database

def getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines):
    checkargs.check(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)

    database = Database()

    importPredefinedSymbols(database, initialDefines)

    return []
