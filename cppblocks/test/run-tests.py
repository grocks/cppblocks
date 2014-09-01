#!/usr/bin/env python
'''
This script runs all the tests in this test suite.
'''

import argparse
import os
import importlib
import re
import sys
import traceback

parser = argparse.ArgumentParser(description='Test framework to validate the output of CppBlocks.')
parser.add_argument('-t', '--tolerance', metavar="NLINES", type=int, action='store', default=0, help='A number of lines that the block returned from CppBlocks might differ in length from the expected block length. (The start line must still be the same. Default: 0)')
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Enable verbose mode. (Default: off)')
parser.add_argument('tests', metavar="TESTS", type=str, action='store', nargs='?', default='.', help='A regular expression to select (a subset of) the test suite. (Default: ".")')
args = parser.parse_args()
tolerance = args.tolerance

# Directory of this script
testDir = os.path.dirname(__file__)

# Add cppblocks directory to list of module search paths
sys.path.append(os.path.join(testDir, '../..'))

import cppblocks

verbose = args.verbose

testCounter = 0

# Print some progress information in case verbose mode is enabled
def information(msg):
    if verbose:
        print msg

def compareBlocks(file, expected, actual):
    if len(expected) != len(actual):
        return False

    for idx in xrange(len(expected)):
        expectedBlock = expected[idx]
        actualBlock = actual[idx]

        # Compare start lines
        if expectedBlock[0] != actualBlock[0]:
            return False

        # Compare for an exact match
        if expectedBlock[1] != actualBlock[1]:
            # Then try a tolerance match block length and account for tolerance
            if abs(expectedBlock[1] - actualBlock[1]) > tolerance:
                return False
            # Notify about tolerance match
            information('    {0}: tolerance match on expected block {1} was {2}'.format(file, expectedBlock, actualBlock))

    return True

def translateToUnixPath(path):
    return path.replace('\\', '/')

def translateFileNames(disabledBlocksDict):
    translatedBlocksDict = {}
    for file in disabledBlocksDict.iterkeys():
        translatedBlocksDict[translateToUnixPath(file)] = disabledBlocksDict[file]
    return translatedBlocksDict

def compareResults(expected, actual):
    if expected.keys() != actual.keys():
        return False

    for path in expected.iterkeys():
        if not compareBlocks(path, expected[path], actual[path]):
            return False

    return True

def runTestCase(testDir, test, name):
    try:
        filepath = os.path.join(testDir, test['input'][0])
        analyzeHeaders = test['input'][1]
        includeDirsAngle = map(lambda path: os.path.join(testDir, path), test['input'][2])
        includeDirsQuote = map(lambda path: os.path.join(testDir, path), test['input'][3])
        initialDefines = test['input'][4]

        disabledBlocks = cppblocks.getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)
        # Translate filepaths back to paths used in the tests
        disabledBlocksRelPaths = {}
        for filepath in disabledBlocks:
            relPath = os.path.relpath(filepath, testDir)
            disabledBlocksRelPaths[relPath] = disabledBlocks[filepath]

        expectedBlocks = translateFileNames(test['expected'])
        disabledBlocksRelPaths = translateFileNames(disabledBlocksRelPaths)

        if not compareResults(expectedBlocks, disabledBlocksRelPaths):
            print "Test failed {0}: '{1}'\nExpected: {2}\nGot: {3}".format(name, test['description'], test['expected'], disabledBlocks)
    except Exception as e:
        print "Test {0}: '{1}' failed!\n".format(name, test['description'])
        print "Reason: {0}".format(e)
        traceback.print_exc(file=sys.stdout)

    global testCounter
    testCounter += 1

def runTestCases(testDir, testCase, name):
    for test in testCase.testCases:
        information('  Test: {0}'.format(test['description']))
        runTestCase(testDir, test, name)

def runTest(testDir, name):
    information('Running test {0}'.format(name))
    # Dynamically load the module from the test directory
    testCase = importlib.import_module(name, testDir)
    runTestCases(testDir, testCase, name)

# Iterate over all directories containing a test and execute them
tests = os.listdir(testDir)
if len(tests) is 0:
    print "No tests found!"
else:
    for testName in tests:
        testCasePath = os.path.join(testDir, testName)
        if os.path.isdir(testCasePath):
            if re.search(args.tests, testCasePath):
                runTest(testCasePath, testName)
    print "Executed {0} test cases".format(testCounter)
