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

verbose = True

# Print some progress information in case verbose mode is enabled
def information(msg):
    if verbose:
        print msg

def runTestCase(test, name):
    if test['expected'] != cppblocks.getDisabledBlocks(*test['input']):
        print "Test failed {0}: '{1}'".format(name, test['description'])

def runTestCases(testDir, testCase, name):
    for test in testCase.testCases:
        information('  Test: {0}'.format(test['description']))
        runTestCase(test, name)

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
