#!/usr/bin/env python
''' The Auto Test Generator generates CppBlocks tests from source code file.

For usage information see the --help output.
'''

import argparse
import os

from autotestgen import makeCppBlocksTest

def filePath(parser, arg):
    ''' Check that argument value is a valid path and return that value. '''
    from os import path
    def checkFilePath(str):
        if not path.exists(str):
            parser.error("argument '{0}' requires a valid file path.".format(arg))
        return str
    return checkFilePath

parser = argparse.ArgumentParser(description='The Auto Test Generator generates CppBlocks tests from source code files.')
parser.add_argument('-I', '--include', metavar="PATH", type=filePath(parser, '--include'), action='append', default=[], help='The directories to search for header files. (Default: no directory)')
parser.add_argument('-o', '--outdir', metavar="DIRPATH", type=filePath(parser, '--outdir'), action='store', default='.', help='The directory to store the test in. (Default: current directory.)')
parser.add_argument('files', metavar="FILE", type=str, nargs='+', help='The source files to generate tests from.')
parser.add_argument('-P', '--cpp', metavar="CPP", type=str, action='store', default='cpp', help='The CPP command that serves as reference for the Auto Test Generator. (Default: cpp)')
parser.add_argument('-r', '--recursive', action='store_true', default=False, help='Perform recursive search for headers in given include directories. (Default: no)')

args = parser.parse_args()

includeDirs = args.include
if args.recursive:
    # To avoid duplicates in our directory list, we use a set
    includeDirs = set()
    for includeDir in args.include:
        # Collect a list of the directory and all subdirectories using os.walk
        includeDirs.update([x[0] for x in os.walk(includeDir)])
    includeDirs = list(includeDirs)

makeCppBlocksTest(outdir=args.outdir, sourceFiles=args.files, includeDirs=includeDirs, preprocessor=args.cpp)
