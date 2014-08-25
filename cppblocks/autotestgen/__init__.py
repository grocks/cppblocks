''' Auto Test Generator

This library implements necessary operations to transform a source code file
into a simplified version for use as a source for automatic test generation.

It expands include directives into the source code files and strips
non-cppdirective lines with line numbers. Adjacent non-cppdirective lines are
collapsed into a single line.

The resulting file is fed to a C preprocessor, e.g., GNU CPP. The C
preprocessor will strip all parts from the file that are excluded from
compilation. Only those lines (with line numbers) will remain, which would be
included into the compilation process.

The Auto Test Generator uses this list of line numbers to create a list of
disabled blocks for use with the CppBlocks testsuite.
'''

from subprocess import check_output as invokeCommand
from os.path import join as pathJoin, basename
import os
import re
import sys

from filefinder import FileFinder, CurDirFileFinder
from autotestgen.ixpand import expandIncludes
from autotestgen.codemangler import replaceNonCppLinesWithLineNumbers

reCompilerDirective = re.compile(r'^\s*\#')
reEmptyLine = re.compile(r'^\s*$')

def makeCppBlocksTest(outdir, sourceFiles, includeDirs, preprocessor='cpp'):
    fileFinderAngleInclude = FileFinder(includeDirs)
    fileFinderQuoteInclude = CurDirFileFinder(includeDirs)


    createTestDirectoryStructure(outdir)

    testCases = []
    idx = 0
    for sourceFile in sourceFiles:
        idx += 1
        inputFilePath = createInputFilePath(sourceFile, idx)

        with createInputFile(outdir, inputFilePath, idx) as f:
            collapsedFile = prepareCollapsedSourceFile(sourceFile, fileFinderAngleInclude, fileFinderQuoteInclude)

            f.write(collapsedFile['text'])
            f.flush()

            activeLines = preprocessFile(f.name, includeDirs, preprocessor)

        allLines = collapsedFile['nonCppLineNumberList']

        disabledBlocks = computeDisabledBlocks(allLines, activeLines)

        testCase = createTestCase(inputFilePath, disabledBlocks)
        testCases.append(testCase)

    writeTestScript(outdir, testCases)

def prepareCollapsedSourceFile(sourceFile, fileFinderAngleInclude, fileFinderQuoteInclude):
        textBlock = expandIncludes(sourceFile, fileFinderAngleInclude, fileFinderQuoteInclude)
        collapsedFile = replaceNonCppLinesWithLineNumbers(textBlock)
        return collapsedFile

def preprocessFile(sourceFile, includeDirs, preprocessor):
    ''' Preprocess given source file.

    Calls the preprocessor on the given source file and cleans up its output.

    Cleanup consists of stripping all empty lines and all lines with compiler
    information (i.e., lines starting with #)

    Returns a list of line numbers that are active.
    '''
    commandLine = [ preprocessor ]
    map(lambda d: commandLine.extend(['-I', d]), includeDirs)
    commandLine.append(sourceFile)

    processedFileContent = invokeCommand(commandLine)

    return cleanFile(processedFileContent)

def cleanFile(processedFileContent):
    lines = processedFileContent.splitlines()
    cleanedLines = []

    for line in lines:
        if reCompilerDirective.match(line) or reEmptyLine.match(line):
            continue
        cleanedLines.append(line)

    return map(int, cleanedLines)

def computeDisabledBlocks(allLines, activeLines):
    return list(set(allLines) - set(activeLines))

def createTestDirectoryStructure(outdir):
    testDir = pathJoin(outdir, 'input')
    retries = 0

    # There is a fundamental race condition between testing and creating a
    # directory. mkdir() will raise an exception if the directory is already
    # created. Since there is no portable way to evaluate the reason for the
    # exception we try to create it in a loop, but no more than two times.
    while not os.path.exists(testDir) and retries < 2:
        try:
            os.mkdir(testDir)
        except OSError:
            retries += 1 # Try again

def createInputFilePath(sourceFile, idx):
    name = basename(sourceFile)
    name = '{0}-{1}'.format(str(idx).zfill(2), name)
    return pathJoin('input', name)

def createInputFile(outdir, sourceFile, idx):
    inputFile = pathJoin(outdir, sourceFile)
    return open(inputFile, 'w+b')

def createTestCase(sourceFile, disabledBlocks):
    return '''    {{
        'description' : 'Auto-generated test.',
        'expected' : {{
            '{0}' : [{1}]
        }},
        'input' : [ '{0}', False, [], [], {{}} ]
    }}'''.format(sourceFile, ", ".join(map(str, disabledBlocks)))

def writeTestScript(outdir, testCases):
    testScript = '''testCases = [
{0}
]'''.format(",\n".join(testCases))
    with open(pathJoin(outdir, '__init__.py'), 'w+b') as f:
        f.write(testScript)
