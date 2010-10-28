#TODO - must finish the compileTerm() method.  This means handling subroutine calls.  
#What I should probably do is implement compileSubroutineCall method (even though it's not 
#explicitly mentioned by the book) and implement what the book says.  This has the added benefit
#that I can replace my subroutine call in compileDo() because it appears to be broken.
class CompilationEngine:

    def __init__(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.outputFile = outputFile
        print(outputFile)
    
    def compileClass(self):
        from JackTokenizer import JackTokenizer
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
            classVarCount += 1
            self.compileClassVarDec()
        while(self.tokenizer.hasMoreTokens() and self.tokenizer.tokenType == JackTokenizer.KEYWORD 
                and self.tokenizer.keyWord() in subOpenings):
            self.compileSubroutine()
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
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<subroutineDec>\n")
        NUM_OPENING_STATEMENTS = 4
        i = 0
        while self.tokenizer.hasMoreTokens() and i < NUM_OPENING_STATEMENTS:
            self.printToken()
            self.tokenizer.advance()
            i += 1
        self.compileParameterList()
        self.printToken() #Should print closing ")" after parameter list
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.compileSubroutineBody()
        self.outputFile.write("</subroutineDec>\n")
    
    def compileSubroutineBody(self):
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<subroutineBody>\n")
        self.printToken() #Should print "{"
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        while(self.tokenizer.hasMoreTokens() and self.tokenizer.tokenType == JackTokenizer.KEYWORD
                and self.tokenizer.keyWord() == "var"):
            self.compileVarDec()
        self.compileStatements()
        self.printToken() #Should print closing "}"
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.outputFile.write("</subroutineBody>\n")

    def compileParameterList(self):
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<parameterList>\n")
        while self.tokenizer.tokenType != JackTokenizer.SYMBOL or self.tokenizer.symbol() != ")":
            boolVal = self.tokenizer.tokenType != JackTokenizer.SYMBOL or self.tokenizer.symbol() != ")"
            self.printToken() #Should print the type or a comma
            if self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ",":
                self.tokenizer.advance()
                self.printToken() #should print the type
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            self.printToken() #Should print the variable name
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance() #should advance to a comma or a closing paren
        self.outputFile.write("</parameterList>\n")

    def compileVarDec(self):
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<varDec>\n")
        while(self.tokenizer.hasMoreTokens() and 
                (self.tokenizer.tokenType != JackTokenizer.SYMBOL or self.tokenizer.symbol() != ";")):
            self.printToken()
            self.tokenizer.advance()
        self.printToken()
        self.tokenizer.advance()
        self.outputFile.write("</varDec>\n")

    def compileStatements(self):
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<statements>\n")
        stmtStarts = ['do', 'while', 'let', 'if', 'return']
        while(self.tokenizer.hasMoreTokens() and self.tokenizer.tokenType == JackTokenizer.KEYWORD 
              and self.tokenizer.keyWord() in stmtStarts):
            print("The current token is " + self.tokenizer.currentToken)
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
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<doStatement>\n")
        if self.tokenizer.keyWord() != "do":
            raise Exception("'do' keyword expected")
        self.printToken()
        while (self.tokenizer.hasMoreTokens() and 
              (self.tokenizer.tokenType != JackTokenizer.SYMBOL or self.tokenizer.symbol() != "(")):
            self.tokenizer.advance() 
            self.printToken()
        self.tokenizer.advance()
        self.compileExpressionList()
        self.printToken() #print ')'
        self.tokenizer.advance()
        self.printToken() #Print ';'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.outputFile.write("</doStatement>\n")

    def compileLet(self):
        self.outputFile.write("<letStatement>\n")
        if self.tokenizer.keyWord() != "let":
            raise Exception("Let keyword expected")
        self.printToken() #Should print "let"
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance() #Should advance to varName
        numOpeningStatements = 2
        i = 0
        while self.tokenizer.hasMoreTokens() and i < numOpeningStatements:
            self.printToken()
            self.tokenizer.advance()
            i += 1
            #TODO - This doesn't currently handle arrays. 
        self.compileExpression()
        self.printToken() #print ";"
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.outputFile.write("</letStatement>\n")

    def compileWhile(self):
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<whileStatement>\n")
        if not(self.tokenizer.tokenType == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "while"):
            raise Exception("'while' keyword was expected")
        self.printToken() #print 'while'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #print '('
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileExpression()
            self.printToken() #print ')'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #print '{'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileStatements()
            self.printToken() #print '}'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.outputFile.write("</whileStatement>\n")

    def compileReturn(self):
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<returnStatement>\n")
        if self.tokenizer.keyWord() != "return":
            raise Exception("'return' keyword was expected")
        self.printToken() #print 'return' keyword
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ";"):
            self.compileExpression()
        self.printToken() #print ";"
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.outputFile.write("</returnStatement>\n")

    def compileIf(self):
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<ifStatement>\n")
        if self.tokenizer.keyWord() != "if":
            raise Exception("'if' keyword was expected")
        self.printToken() #print 'if'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #print '('
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileExpression()
            self.printToken() #print ')'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #print '{'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileStatements()
            self.printToken() #print '}'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        if not(self.tokenizer.tokenType == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "else"):
            self.outputFile.write("</ifStatement>\n")
            return
        self.printToken() #print 'else'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #print '{'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileStatements()
        self.printToken() #print '}'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.outputFile.write("</ifStatement>\n")

    def compileExpression(self):
        from JackTokenizer import JackTokenizer
        opList = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        self.outputFile.write("<expression>\n")
        self.compileTerm()
        while self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() in opList:
            self.printToken()
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.compileTerm()
        self.outputFile.write("</expression>\n")

    def compileTerm(self):
        from JackTokenizer import JackTokenizer
        unaryOps = ['-', '~']
        self.outputFile.write("<term>\n")
        self.printToken()
        if self.tokenizer.tokenType == JackTokenizer.IDENTIFIER:
            self.tokenizer.advance()
            self.printToken()
            if self.tokenizer.tokenType == JackTokenizer.SYMBOL:
        elif self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == "(":
            self.tokenizer.advance()
            self.compileExpression()
            self.printToken() #print ')'
        elif self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() in unaryOps:
            self.tokenizer.advance()
            self.compileTerm()
        self.outputFile.write("</term>\n")

    def compileExpressionList(self):
        from JackTokenizer import JackTokenizer
        self.outputFile.write("<expressionList>\n")
        #I sort of feel guilty for doing this since this relies on knowing that
        #the expression list is surrounded by parenthesis and according to the spec
        #it should not know that (it would require modifying this message if I wanted to use an expression list anywhere else).
        #However, also according to the spec I should create a <subroutineCall> XML element
        while not(self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ")"):
           self.compileExpression() 
           if self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ",":
               self.printToken() #print ','
               if self.tokenizer.hasMoreTokens():
                   self.tokenizer.advance()
        self.outputFile.write("</expressionList>\n")

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
