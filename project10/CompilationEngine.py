class CompilationEngine:

    def __init__(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.outputFile = outputFile
        print(outputFile)
    
    def compileClass(self):
        NUM_OPENING_STATEMENTS = 3
        classVarOpenings = ['static', 'field']
        subOpenings = ['constructor', 'function', 'method']

        if self.tokenizer.currentToken != "class":
            raise Exception("Keyword 'class' expected")
        self.outputFile.write("<class>\n")
        i = 0
        while self.tokenizer.hasMoreTokens() and i < NUM_OPENING_STATEMENTS: 
            self.printToken()
            self.tokenizer.advance()
            i += 1
        
        classVarCount = 0
        while self.tokenizer.hasMoreTokens() and self.tokenizer.keyWord() in classVarOpenings:
            print("ClassVarCount is " + str(classVarCount))
            classVarCount += 1
            self.compileClassVarDec()
            print("Token after class is - " + self.tokenizer.currentToken)
        while self.tokenizer.hasMoreTokens() and self.tokenizer.keyWord in subOpenings:
            self.compileSubroutine()
            print("compile subroutine should have been called")
        self.printToken()
        self.outputFile.write("</class>\n")
    
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
            self.printToken()
            self.tokenizer.advance()
            self.printToken()
            if not self.tokenizer.hasMoreTokens():
                raise Exception("Another variable expected in list")
            self.tokenizer.advance()
        self.printToken()

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
        while(self.tokenizer.hasMoreTokens() and 
                (self.tokenizer.tokenType != JackTokenizer.SYMBOL or self.tokenizer.symbol() != ";")):
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
        self.outputFile.write("<doStatement>\n")
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
        #Not implemented until tested with Square Dance
        self.outputFile.write("<letStatement>\n")
        if self.tokenizer.keyWord() != "let":
            raise Exception("Let keyword expected")
        self.printToken()
        while self.tokenizer.hasMoreTokens() and self.tokenizer.tokenType():
            pass
            #TODO - put in later
        self.outputFile.write("</letStatement>\n")

    def compileWhile(self):
        pass
        #Not implemented until tested with Square Dance

    def compileReturn(self):
        pass
        #Not implemented until tested with Square Dance

    def compileIf(self):
        pass
        #Not implemented until tested with Square Dance

    def compileExpression(self):
        pass
        #Not implemented until tested with Square Dance

    def compileTerm(self):
        self.outputFile.write("<term>")
        self.printToken()
        currentType = self.tokenizer.tokenType()
        self.tokenizer.advance()
        if currentType == JackTokenizer.IDENTIFIER:
            if self.tokenizer.tokenType == JackTokenizer.SYMBOL:
                pass
                #Requires expression, not implemented yet
        elif currentType == JackTokenizer.SYMBOL:
            self.compileTerm()
        self.outputFile.write("</term>")

    def compileExpressionList(self):
        pass
        #Not implemented until tested with Square Dance
    
    def printToken(self):
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
