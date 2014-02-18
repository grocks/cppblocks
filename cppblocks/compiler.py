'''
A compiler for disabled CPP conditional blocks.

The compiler walks the AST generated by CppParser using the tree visitor from
the Spark framework.
'''

class DisabledBlocksCompiler:
    def __init__(self, filepath, analyzeHeaders, database, fileFinderAngleInclude, fileFinderQuoteInclude, astRootNode):
        self.filepath = filepath
        self.analyzeHeaders = analyzeHeaders
        self.symbols = database
        self.fileFinderAngleInclude = fileFinderAngleInclude
        self.fileFinderQuoteInclude = fileFinderQuoteInclude
        self.rootNode = astRootNode
        self.disabledBlocks = { self.filepath : [] }

        self.visitorMap = {
                'ifSection' : self.v_ifSection,
                'ifdef' : self.v_ifdef,
                'ifndef' : self.v_ifndef,
                'if' : self.v_if,
                'define' : self.v_define,
                'undef' : self.v_undef,
                'includeAngle' : self.v_includeAngle,
                'includeQuote' : self.v_includeQuote
        }

    def getDisabledBlocks(self):
        if self.rootNode:
            self.traversePreorder(self.rootNode)
        return self.disabledBlocks

    def traversePreorder(self, node):
        children = []

        visitChildren = self.visit(node)

        if type(visitChildren) is list:
            children = visitChildren # Visitor returned a list of children to process
        elif visitChildren: # Visitor wants to visit its children
            children = node.children

        for child in children:
            self.traversePreorder(child)

        for sibling in node.siblings:
            self.traversePreorder(sibling)

    def visit(self, node):
        if not node.typ in self.visitorMap:
            raise UnsupportedToken(node)
        visitor = self.visitorMap[node.typ]
        return visitor(node)

    def v_ifdef(self, node):
        return self.symbols.defined(node.symbol)

    def v_ifndef(self, node):
        return not self.symbols.defined(node.symbol)

    def v_if(self, node):
        if node.expression[0].isdigit():
            expr = node.expression
        else:
            expr = self.symbols.getValue(node.expression)

        return int(expr)

    def v_ifSection(self, node):
        ifCondResult = self.visit(node.ifGroup)
        if ifCondResult:
            if node.elseGroup:
                self.addDisabledBlock(node.elseGroup.line, node.elseGroup.length)
            return node.ifGroup.children
        else:
            self.addDisabledBlock(node.ifGroup.line, node.ifGroup.length)
            if node.elseGroup:
                return node.elseGroup.children
        # Never visit any children of v_ifSection unless we explicitly return a list of children
        return False

    def v_define(self, node):
        self.symbols.add(node.name, node.value)

    def v_undef(self, node):
        self.symbols.remove(node.symbol)

    def v_includeAngle(self, node):
        includePath = self.fileFinderAngleInclude.lookup(node.path)
        self.v_include(includePath)

    def v_includeQuote(self, node):
        includePath = self.fileFinderQuoteInclude.lookup(self.filepath, node.path)
        self.v_include(includePath)

    def v_include(self, includePath):
        # Be careful with this cyclic import. See http://stackoverflow.com/questions/11698530/two-python-modules-require-each-others-contents-can-that-work
        from analyzer import analyzeFile
        disabledBlocks = analyzeFile(includePath, self.analyzeHeaders, self.fileFinderAngleInclude, self.fileFinderQuoteInclude, self.symbols)

        if self.analyzeHeaders:
            self.disabledBlocks.update(disabledBlocks)

    def addDisabledBlock(self, start, length):
        ' By convention the first entry in disabledBlocks is always for the file we were invoked on. '
        self.disabledBlocks[self.filepath].append( (start,length) )

