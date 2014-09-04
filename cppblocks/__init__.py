'''
getDisabledBlocks
'''

import trace
def log(*args):
    trace.trace('cppblocks.main', *args)

from checkargs import check as checkArgs
from predefines import importPredefinedSymbols
from database import Database
from filefinder import FileFinder, CurDirFileFinder
from analyzer import analyzeFile

def getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines):
    log('filepath: {0}'.format(filepath),
        'analyzeHeaders: {0}'.format(analyzeHeaders),
        'includeDirsAngle: {0}'.format(includeDirsAngle),
        'includeDirsQuote: {0}'.format(includeDirsQuote),
        'initialDefines: {0}'.format(initialDefines))

    checkargs.check(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)

    symbolDatabase = Database()
    importPredefinedSymbols(symbolDatabase, initialDefines)

    fileFinderAngleInclude = FileFinder(includeDirsAngle)
    fileFinderQuoteInclude = CurDirFileFinder(includeDirsQuote)

    disabledBlocks = analyzeFile(filepath, analyzeHeaders, fileFinderAngleInclude, fileFinderQuoteInclude, symbolDatabase)

    return disabledBlocks
