'''
The class FileFinder manages a list of paths and performs file lookups among them.
'''

from os.path import join as pathJoin, exists as pathExists, realpath, dirname

from messages import FileNotFound

class FileFinder:
    def __init__(self, pathList):
        self.pathList = pathList

    def lookup(self, path):
        candidates = map(lambda stem: pathJoin(stem, path), self.pathList)

        for candidate in candidates:
            if pathExists(candidate):
                return candidate

        raise FileNotFound(path)

    def prepend(self, path):
        self.pathList.insert(0, path)

    def append(self, path):
        self.pathList.append(path)

    def dropFirstPath(self, path):
        ' Remove the path with highest priority during lookup. '
        del self.pathList[0]

class CurDirFileFinder(FileFinder):
    def __init__(self, pathList):
        FileFinder.__init__(self, pathList)
        self.currentDir = None

    def lookup(self, curDirFilePath, path):
        candidate = pathJoin(dirname(curDirFilePath), path)
        if pathExists(candidate):
            return candidate
        return FileFinder.lookup(self, path)
