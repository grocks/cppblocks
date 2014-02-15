#!/usr/bin/env python
'''
This script runs all the tests in this test suite.
'''

import os
import importlib
import sys


# Directory of this script
testDir = os.path.dirname(__file__)

# Add cppblocks directory to list of module search paths
sys.path.append(os.path.join(testDir, '../..'))

import cppblocks

#verbose = True
verbose = False

# Print some progress information in case verbose mode is enabled
def information(msg):
    if verbose:
        print msg

def runTestCase(testDir, test, name):
    filepath = os.path.join(testDir, test['input'][0])
    analyzeHeaders = test['input'][1]
    includeDirsAngle = test['input'][2]
    includeDirsQuote = test['input'][3]
    initialDefines = test['input'][4]

    disabledBlocks = cppblocks.getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)
    # Translate filepaths back to paths used in the tests
    for block in disabledBlocks:
        block['filepath'] = os.path.relpath(block['filepath'], testDir)

    if test['expected'] != disabledBlocks:
        print "Test failed {0}: '{1}'\nExpected: {2}\nGot: {3}".format(name, test['description'], test['expected'], disabledBlocks)

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
for name in os.listdir(testDir):
    testCasePath = os.path.join(testDir, name)
    if os.path.isdir(testCasePath):
        runTest(testCasePath, name)
