'''
getDisabledBlocks
'''

from checkargs import check as checkArgs
from predefines import importPredefinedSymbols
from database import Database
from filefinder import FileFinder, CurDirFileFinder
from analyzer import analyzeFile

def getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines):
    checkargs.check(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)

    symbolDatabase = Database()
    importPredefinedSymbols(symbolDatabase, initialDefines)

    fileFinderAngleInclude = FileFinder(includeDirsAngle)
    fileFinderQuoteInclude = CurDirFileFinder(includeDirsQuote)

    disabledBlocks = analyzeFile(filepath, analyzeHeaders, fileFinderAngleInclude, fileFinderQuoteInclude, symbolDatabase)

    return disabledBlocks
