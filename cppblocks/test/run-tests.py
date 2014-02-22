#!/usr/bin/env python
'''
This script runs all the tests in this test suite.
'''

import os
import importlib
import re
import sys


# Directory of this script
testDir = os.path.dirname(__file__)

# Add cppblocks directory to list of module search paths
sys.path.append(os.path.join(testDir, '../..'))

import cppblocks

#verbose = True
verbose = False

testCounter = 0

# Print some progress information in case verbose mode is enabled
def information(msg):
    if verbose:
        print msg

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

        if test['expected'] != disabledBlocksRelPaths:
            print "Test failed {0}: '{1}'\nExpected: {2}\nGot: {3}".format(name, test['description'], test['expected'], disabledBlocks)
    except:
        print "Test {0}: '{1}' failed!\n".format(name, test['description'])

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

# Provide default criteria if the user did not provide a match pattern.
if len(sys.argv) == 1:
    sys.argv.append('.')

# Iterate over all directories containing a test and execute them
tests = os.listdir(testDir)
if len(tests) is 0:
    print "No tests found!"
else:
    for testName in tests:
        testCasePath = os.path.join(testDir, testName)
        if os.path.isdir(testCasePath):
            if re.search(sys.argv[1], testCasePath):
                runTest(testCasePath, testName)
    print "Executed {0} test cases".format(testCounter)
