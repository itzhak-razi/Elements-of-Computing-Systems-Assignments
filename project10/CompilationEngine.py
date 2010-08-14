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
        self.outputFile.write("<class>\n")
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
        outputFile.write("</class>\n")
    
    def compileClassVarDec(self):
        self.outputFile.write("<classVarDec>\n")
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
        self.outputFile.write("</classVarDec>\n")

    def compileSubroutine(self):
        self.outputFile.write("<subroutineDec>\n")
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
        self.outputFile.write("</subroutineDec>\n")

    def compileParameterList(self):
        import JackTokenizer
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<parameterList>\n")
        while self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() != ")":
            self.printToken()
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            self.printToken()
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            self.printToken()
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
        self.outputFile.write("</parameterList>\n")

    def compileVarDec(self):
        self.outputFile.write("<varDec>\n")
        while self.tokenizer.hasMoreTokens() and 
                (self.tokenizer.tokenType != JackTokenizer.SYMBOL or self.tokenizer.symbol() != ";"):
            self.printToken()
            self.tokenizer.advance()
        self.printToken()
        self.tokenizer.advance()
        self.outputFile.write("</varDec>\n")

    def compileStatements(self):
        self.outputFile.write("<statements>\n")
        stmtStarts = ['do', 'while', 'let', 'if', 'return']
        while(self.tokenizer.hasMoreTokens() and self.tokenizer.tokenType == JackTokenizer.KEYWORD 
              and self.tokenizer.keyWord() in stmtStarts):
            if self.tokenizer.keyWord() == "do":
                self.compileDo()
            elif self.tokenizer.keyWord() == "while":
                self.compileWhile()
            elif self.tokenizer.keyWord() == "let":
                self.compileLet()
            elif self.tokenizer.keyWord() == "if":
                self.compileIf()
            elif self.tokenizer.keyWord() == "return":
                self.compileReturn()
        self.outputFile.write("</statements>\n")

    def compileDo(self):
        self.outputFile.write("</doStatement>\n")
        if self.tokenizer.keyWord() != "do":
            raise Exception("'do' keyword expected")
        self.printToken()
        while (self.tokenizer.hasMoreTokens() and 
              (self.tokenizer.tokenType != JackTokenizer.SYMBOL or JackTokenizer.tokenType.symbol() != "(")):
            self.tokenizer.advance() 
            self.printToken()
        self.compileExpressionList()
        self.printToken() #print ')'
        self.tokenizer.advance()
        self.printToken() #Print ';'
        self.outputFile.write("</doStatement>\n")

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
