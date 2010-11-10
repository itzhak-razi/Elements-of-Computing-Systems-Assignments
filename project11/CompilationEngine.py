#TODO - handle subroutine and clases.  Should write info about them when they're being defined or called
class CompilationEngine:

    keywordConsts = ["null", "true", "false", "this"] 
    def __init__(self, tokenizer, outputFile, vmFile):
        from SymbolTable import SymbolTable
        from VMWriter import VMWriter
        self.tokenizer = tokenizer
        self.outputFile = outputFile
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(vmFile)
        print(outputFile)
    
    def compileClass(self):
        from JackTokenizer import JackTokenizer
        self.indentLevel = 0
        NUM_OPENING_STATEMENTS = 3
        classVarOpenings = ['static', 'field']
        subOpenings = ['constructor', 'function', 'method']

        if self.tokenizer.currentToken != "class":
            raise Exception("Keyword 'class' expected")
        self.writeFormatted("<class>")
        self.indentLevel += 1
        self.printToken() #Should print 'class'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print class name
            self.writeClassOrSubInfo("class", False)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print '{'
        
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        
        classVarCount = 0
        while self.tokenizer.hasMoreTokens() and self.tokenizer.keyWord() in classVarOpenings:
            classVarCount += 1
            self.compileClassVarDec()
        while(self.tokenizer.hasMoreTokens() and self.tokenizer.tokenType == JackTokenizer.KEYWORD 
                and self.tokenizer.keyWord() in subOpenings):
            self.compileSubroutine()
        self.printToken()
        self.writeFormatted("</class>")
        self.indentLevel -= 1
    
    def compileClassVarDec(self):
        from JackTokenizer import JackTokenizer
        from SymbolTable import SymbolTable 
        self.writeFormatted("<classVarDec>")
        self.indentLevel += 1
        self.printToken() #Should print static or field
        if self.tokenizer.tokenType == JackTokenizer.KEYWORD:
            if self.tokenizer.keyWord() == "static":
                kind = SymbolTable.STATIC
            elif self.tokenizer.keyWord() == "field":
                kind = SymbolTable.FIELD
            else:
                raise Exception("Invalid kind of class variable " + self.tokenizer.keyWord())
        else:
            raise Exception("Keyword expected")
        
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print the variable type
            identifierType = self.tokenizer.currentToken
            isKeyword = self.tokenizer.tokenType == JackTokenizer.KEYWORD

        if not isKeyword:
            self.writeClassOrSubInfo("class", True)

        varNames = []
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print variable name
            varNames.append(self.tokenizer.currentToken)
            if self.tokenizer.hasMoreTokens(): 
                self.tokenizer.advance()

        while self.tokenizer.symbol() != ";" and self.tokenizer.hasMoreTokens():
            if self.tokenizer.symbol() != ",":
                raise Exception("Invalid variable list")
            self.printToken() #Should print ','
            self.tokenizer.advance()
            self.printToken() #Should print variable name
            varNames.append(self.tokenizer.currentToken)
            if not self.tokenizer.hasMoreTokens():
                raise Exception("More tokens expected")
            self.tokenizer.advance()
        self.printToken()
    

        for name in varNames:
            self.symbolTable.define(name, identifierType, kind)
            self.writeVarInfo(name, False)


        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.indentLevel -= 1
        self.writeFormatted("</classVarDec>")

    def compileSubroutine(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<subroutineDec>")
        self.symbolTable.startSubroutine()
        self.indentLevel += 1
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
        self.indentLevel -= 1
        self.writeFormatted("</subroutineDec>")
    
    def compileSubroutineBody(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<subroutineBody>")
        self.indentLevel += 1
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
        self.indentLevel -= 1
        self.writeFormatted("</subroutineBody>")

    def compileParameterList(self):
        from JackTokenizer import JackTokenizer
        from SymbolTable import SymbolTable
        self.writeFormatted("<parameterList>")
        self.indentLevel += 1

        if self.tokenizer.currentToken != ")":
            self.printToken() #Should print the type
            argType = self.tokenizer.currentToken
            self.tokenizer.advance()
            self.printToken() #Should print the name
            argName = self.tokenizer.currentToken
            self.symbolTable.define(argName, argType, SymbolTable.ARG)
            self.writeVarInfo(argName, False)
            self.tokenizer.advance()


        while self.tokenizer.tokenType != JackTokenizer.SYMBOL or self.tokenizer.symbol() != ")":
            self.printToken() #Should print a comma
            if self.tokenizer.currentToken != ",":
                raise Exception("Comma expected")
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.printToken() #Should print the argument type
                argType = self.tokenizer.currentToken
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.printToken() #Should print the argument name
                argName = self.tokenizer.currentToken
                self.symbolTable.define(argName, argType, SymbolTable.ARG)
                self.writeVarInfo(argName, False)
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            
        self.indentLevel -= 1
        self.writeFormatted("</parameterList>")

    def compileVarDec(self):
        from JackTokenizer import JackTokenizer
        from SymbolTable import SymbolTable
        self.writeFormatted("<varDec>")
        self.indentLevel += 1
        
        varNames = []
        self.printToken() #Should print 'var'
        if self.tokenizer.currentToken != "var":
            raise Exception("'var' keyword expected")
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print the type
            varType = self.tokenizer.currentToken
            isKeyword = self.tokenizer.tokenType == JackTokenizer.KEYWORD

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance() 
            self.printToken() #Should print the var name
            varNames.append(self.tokenizer.currentToken) 
        
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

        while(self.tokenizer.hasMoreTokens() and 
                (self.tokenizer.tokenType != JackTokenizer.SYMBOL or self.tokenizer.symbol() != ";")):
            self.printToken() #Should print ','
            self.tokenizer.advance()
            self.printToken() #Should print the var name
            varNames.append(self.tokenizer.currentToken)
            self.tokenizer.advance()
        
        #If the type is not a keyword (e.g. int) that means it's a class and we should print identifier info
        if not isKeyword:
            self.writeClassOrSubInfo("class", "True")

        for name in varNames:
            self.symbolTable.define(name, varType, SymbolTable.VAR)
            self.writeVarInfo(name, False)

        self.printToken() #Should print ';'
        self.tokenizer.advance()
        self.indentLevel -= 1
        self.writeFormatted("</varDec>")

    def compileStatements(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<statements>")
        self.indentLevel += 1
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
        self.indentLevel -= 1
        self.writeFormatted("</statements>")

    def compileDo(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<doStatement>")
        self.indentLevel += 1
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
        self.indentLevel -= 1
        self.writeFormatted("</doStatement>")

    def compileLet(self):
        self.writeFormatted("<letStatement>")
        self.indentLevel += 1
        if self.tokenizer.keyWord() != "let":
            raise Exception("Let keyword expected")
        self.printToken() #Should print "let"
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print varname
            self.writeVarInfo(self.tokenizer.identifier(), True)
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            print("compileLet - [ or = " + self.tokenizer.currentToken)
            self.printToken() #Should print '[' or '='
        if self.tokenizer.currentToken == "[":
            self.tokenizer.advance()
            self.compileExpression()
            self.printToken() #Should print ']'
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.printToken() #Should print '='
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        print("compileLet - after equals " + self.tokenizer.currentToken)
        self.compileExpression()
        self.printToken() #print ";"
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.indentLevel -= 1
        self.writeFormatted("</letStatement>")

    def compileWhile(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<whileStatement>")
        self.indentLevel += 1
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
        self.indentLevel -= 1
        self.writeFormatted("</whileStatement>")

    def compileReturn(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<returnStatement>")
        self.indentLevel += 1
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
        self.indentLevel -= 1
        self.writeFormatted("</returnStatement>")

    def compileIf(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<ifStatement>")
        self.indentLevel += 1
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
            self.writeFormatted("</ifStatement>")
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
        self.indentLevel -= 1
        self.writeFormatted("</ifStatement>")

    def compileExpression(self):
        from JackTokenizer import JackTokenizer
        opList = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
        self.writeFormatted("<expression>")
        self.indentLevel += 1
        print("About to call compile term current token is " + self.tokenizer.currentToken)
        self.compileTerm()
        while self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() in opList:
            self.printToken()
            print("Current operator " + self.tokenizer.currentToken)
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.compileTerm()
        self.indentLevel -= 1
        self.writeFormatted("</expression>")

    def compileTerm(self):
        from JackTokenizer import JackTokenizer
        print("Opening token is " + self.tokenizer.currentToken)
        unaryOps = ['-', '~']
        self.writeFormatted("<term>")
        self.indentLevel += 1
        self.printToken()
        if self.tokenizer.tokenType == JackTokenizer.IDENTIFIER:
            name = self.tokenizer.identifier()
            self.tokenizer.advance()
            print("second token in IDENTIFIER " + self.tokenizer.currentToken)
            if self.tokenizer.tokenType == JackTokenizer.SYMBOL:
                if self.tokenizer.symbol() == ".":

                    if self.symbolTable.isDefined(name):
                        self.writeVarInfo(name, inUse)
                    else:
                        self.writeClassOrSubInfo("class", True)

                    self.printToken()
                    print("Doing the dot thing")
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                        print("Token before doing subroutine call " + self.tokenizer.currentToken)
                        self.compileSubroutineCall()
                        print("Current token after compiling subroutine is " + self.tokenizer.currentToken)
                elif self.tokenizer.symbol() == "(":
                    self.printToken()
                    self.writeClassOrSubInfo("subroutine", True)
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                        self.compileExpressionList()
                        self.printToken() #Print ')'
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                elif self.tokenizer.symbol() == "[":
                    self.writeVarInfo(name, True)
                    self.printToken()
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                        self.compileExpression()
                        self.printToken() #Should print ']'
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                else:
                    self.writeVarInfo(name, True)
        elif self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == "(":
            self.tokenizer.advance()
            print("second token in ()" + self.tokenizer.currentToken)
            self.compileExpression()
            self.printToken() #print ')'
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
        elif self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() in unaryOps:
            self.tokenizer.advance()
            print("second token in unary " + self.tokenizer.currentToken)
            self.compileTerm()
        elif(self.tokenizer.currentToken in CompilationEngine.keywordConsts or 
                self.tokenizer.tokenType == JackTokenizer.INT_CONST or 
                self.tokenizer.tokenType == JackTokenizer.STRING_CONST):
            if self.tokenizer.hasMoreTokens():
               self.tokenizer.advance() 
        else:
            raise Exception("Invalid term provided")
        print("The current token is " + self.tokenizer.currentToken)
        self.indentLevel -= 1
        self.writeFormatted("</term>")

    def compileExpressionList(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<expressionList>")
        self.indentLevel += 1
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
        self.indentLevel -= 1
        self.writeFormatted("</expressionList>")

    def compileSubroutineCall(self):
        from JackTokenizer import JackTokenizer
        self.printToken() #Should print either the subroutine name or the class/object the
        #subroutine is a member of
        firstToken = self.tokenizer.currentToken
        isClassOrObj = False
        print("Subroutine name should be - " + self.tokenizer.currentToken)
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print '.' or '(' 
            print("After subroutine name - " + self.tokenizer.currentToken)
        if self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ".":
            isClassOrObj = True
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance() 
                self.printToken() #Should print subroutine name
                print("Subroutine name - " + self.tokenizer.currentToken)
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.printToken() #Should print opening '('
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileExpressionList()
            self.printToken() #Should print ')'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

        if isClassOrObj and self.symbolTable.isDefined(firstToken):
            self.writeVarInfo(classToken, True) #Writing information about an object
        elif isClassOrObj:
            writeClassOrSubInfo("class", True) #Writing information about a class
        self.writeClassOrSubInfo("subroutine", True)

    def printToken(self):
        from JackTokenizer import JackTokenizer
        if self.tokenizer.tokenType == JackTokenizer.KEYWORD:
           self.writeFormatted("<keyword>" + self.tokenizer.keyWord() + "</keyword>")
        elif self.tokenizer.tokenType == JackTokenizer.SYMBOL:
            self.writeFormatted("<symbol>" + self.tokenizer.symbol() + "</symbol>")
        elif self.tokenizer.tokenType == JackTokenizer.IDENTIFIER:
            self.writeFormatted("<identifier>" + self.tokenizer.identifier() + "</identifier>")
        elif self.tokenizer.tokenType == JackTokenizer.INT_CONST:
            self.writeFormatted("<integerConstant>" + self.tokenizer.intVal() + "</integerConstant>")
        elif self.tokenizer.tokenType == JackTokenizer.STRING_CONST:
            self.writeFormatted("<stringConstant>" + self.tokenizer.stringVal() + "</stringConstant>")

    def writeFormatted(self, string):
        self.outputFile.write("  " * self.indentLevel + string + "\n")
    
    def writeVarInfo(self, varName, inUse):
        from SymbolTable import SymbolTable
        self.writeFormatted("<IdentifierInfo>")
        self.indentLevel += 1
        self.writeFormatted("<type>" + self.symbolTable.typeOf(varName) + "</type>")
        self.writeFormatted("<kind>" + self.symbolTable.stringKindOf(varName) + "</kind>")
        self.writeFormatted("<index>" + str(self.symbolTable.indexOf(varName)) + "</index>")
        self.writeFormatted("<inUse>" + str(inUse) + "</inUse>")
        self.indentLevel -= 1
        self.writeFormatted("</IdentifierInfo>")

    def writeClassOrSubInfo(self, kind, inUse):
       self.writeFormatted("<IdentifierInfo>")
       self.indentLevel += 1
       self.writeFormatted("<kind>" + kind + "</kind>")
       self.writeFormatted("<inUse>" + str(inUse) + "</inUse>")
       self.indentLevel -= 1
       self.writeFormatted("</IdentifierInfo>")
