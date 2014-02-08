'''
getDisabledBlocks
'''

from checkargs import check as checkArgs

def getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines):
    checkargs.check(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)
    return []
