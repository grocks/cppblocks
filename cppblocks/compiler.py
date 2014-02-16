'''
A compiler for disabled CPP conditional blocks.

The compiler walks the AST generated by CppParser using the tree visitor from
the Spark framework.
'''

class DisabledBlocksCompiler:
    def __init__(self, filepath, database, astRootNode):
        self.filepath = filepath
        self.symbols = database
        self.rootNode = astRootNode
        self.disabledBlocks = []

        self.visitorMap = {
                'ifdef' : self.v_ifdef,
                'ifndef' : self.v_ifndef,
                'define' : self.v_define
        }

    def getDisabledBlocks(self):
        if self.rootNode:
            self.traversePreorder(self.rootNode)
        return [ { 'filepath' : self.filepath,
                   'disabledBlocks' : self.disabledBlocks } ]

    def traversePreorder(self, node):
        visitChildren = self.visit(node)

        if visitChildren:
            for child in node.children:
                self.traversePreorder(child)

        for sibling in node.siblings:
            self.traversePreorder(sibling)

    def visit(self, node):
        if not node.typ in self.visitorMap:
            raise UnsupportedToken(node)
        visitor = self.visitorMap[node.typ]
        return visitor(node)

    def v_ifdef(self, node):
        if not self.symbols.defined(node.symbol):
            self.addDisabledBlock(node.line, node.length)
            return False
        return True

    def v_ifndef(self, node):
        if self.symbols.defined(node.symbol):
            self.addDisabledBlock(node.line, node.length)
            return False
        return True

    def v_define(self, node):
        self.symbols.add(node.name, node.value)

    def addDisabledBlock(self, start, length):
        self.disabledBlocks.append( (start,length) )