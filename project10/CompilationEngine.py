class CompilationEngine:

    def __init(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.outputFile = outputFile
    
    def compileClass(self):
        NUM_OPENING_STATEMENTS = 3
        classVarOpenings = ['static', 'field']
        subOpenings = ['constructor', 'function', 'method']

        if tokenizer.currentToken != "class":
            raise Exception("Keyword 'class' expected")
        outputFile.write("<class>\n")
        i = 0
        while tokenizer.hasMoreTokens() and i < NUM_OPENING_STATEMENTS: 
            self.printToken()
            self.tokenizer.advance()
            i += 1
        
        while self.tokenizer.hasMoreTokens() and self.tokenizer.keyWord() in classVarOpenings:
            self.compileClassVarDec()
        while self.tokenizer.hasMoreTokens() and self.tokenizer.keyWord in subOpenings:
            self.compileSubroutine()
        self.printToken()
    
    def compileClassVarDec(self):
        NUM_OPENING_STATEMENTS = 3
        i = 0
        while self.tokenizer.hasMoreTokens() and i < NUM_OPENING_STATEMENTS:
            self.printToken()
            self.tokenizer.advance()
            i += 1
    
        while self.tokenizer.symbol() != ";" and self.tokenizer.hasMoreTokens():
            if self.tokenizer.symbol() != ",":
                raise Exception("Invalid variable list")
            self.tokenizer.printToken()
            self.tokenizer.advance()
            self.tokenizer.printToken()
            if not self.tokenizer.hasMoreTokens():
                raise Exception("Another variable expected in list")
            self.tokenizer.advance()
        self.tokenizer.printToken()

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def compileSubroutine(self):
        NUM_OPENING_STATEMENTS = 4
        i = 0
        while self.tokenizer.hasMoreTokens() and i < NUM_OPENING_STATEMENTS:
            self.printToken()
            self.tokenizer.advance()
            i += 1

        self.compileParameterList()
        self.printToken()
        self.tokenizer.advance()
        while self.tokenizer.hasMoreTokens() and self.tokenizer.keyWord() == "var":
            self.compileVarDec()
        self.compileStatements()
        self.printToken()
        self.tokenizer.advance()



    def compileParameterList(self):

    def compileVarDec(self):

    def compileStatements(self):

    def compileDo(self):

    def compileLet(self):

    def compileWhile(self):

    def compileReturn(self):

    def compileIf(self):

    def compileExpression(self):

    def compileTerm(self):

    def compileExpressionList(self):
    
    def printToken(self):
        import JackTokenizer
        from JackTokenizer import JackTokenizer
        if self.tokenizer.tokenType == JackTokenizer.KEYWORD:
           self.outputFile.write("\t<keyword>" + self.tokenizer.keyWord() + "</keyword>\n")
        elif self.tokenizer.tokenType == JackTokenizer.SYMBOL:
            self.outputFile.write("\t<symbol>" + self.tokenizer.symbol() + "</symbol>\n")
        elif self.tokenizer.tokenType == JackTokenizer.IDENTIFIER:
            self.outputFile.write("\t<identifier>" + self.tokenizer.identifier() + "</identifier>\n")
        elif self.tokenizer.tokenType == JackTokenizer.INT_CONST:
            self.outputFile.write("\t<integerConstant>" + self.tokenizer.intVal() + "</integerConstant>\n")
        elif self.tokenizer.tokenType == JackTokenizer.STRING_CONST:
            self.outputFile.write("\t<stringConstant>" + self.tokenizer.stringVal() + "</stringConstant>\n")
