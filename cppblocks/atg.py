#!/usr/bin/env python
''' The Auto Test Generator generates CppBlocks tests from source code file.

For usage information see the --help output.
'''

import argparse

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

args = parser.parse_args()

makeCppBlocksTest(outdir=args.outdir, sourceFiles=args.files, includeDirs=args.include, preprocessor=args.cpp)
