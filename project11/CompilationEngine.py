class CompilationEngine:

    keywordConsts = ["null", "true", "false", "this"] 
    def __init__(self, tokenizer, outputFile, vmFile):
        from SymbolTable import SymbolTable
        from VMWriter import VMWriter
        self.tokenizer = tokenizer
        self.outputFile = outputFile
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(vmFile)
        self.labelNum = 0
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
            self.className = self.tokenizer.identifier()
            self.writeClassOrSubInfo("class", False)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print '{'
        
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        
        self.classVarCount = 0
        while self.tokenizer.hasMoreTokens() and self.tokenizer.keyWord() in classVarOpenings:
            self.classVarCount += 1
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
        
        self.printToken() #Should print 'constructor', 'function', or 'method'
        
        if self.tokenizer.keyWord() == "constructor":
            self.vmWriter.writePush("constant", self.classVarCount)
            self.vmWriter.writeCall("Memory.alloc", 1) #allocate space for this object
            self.vmWriter.writePop("pointer", 0) #assign object to 'this'

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance() 
            self.printToken() #Should print the type or 'void'

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance() 
            self.printToken() #Should print the subroutine name
            self.subName = self.tokenizer.identifier()

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance() 
            self.printToken() #Should print opening '(' before parameter list

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance() 
        self.compileParameterList()
        self.printToken() #Should print closing ")" after parameter list
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

        self.numLocalVariables = 0
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
        
        self.vmWriter.writeFunction(self.className + "." + self.subName, self.numLocalVariables) 
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
        self.numLocalVariables += 1
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
            self.numLocalVariables += 1
        
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

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileSubroutineCall()
            self.vmWriter.writePop("temp", 0) #This pops and ignores the returned value 

        self.printToken() #Print ';'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.indentLevel -= 1
        self.writeFormatted("</doStatement>")

    def compileLet(self):
        from SymbolTable import SymbolTable
        self.writeFormatted("<letStatement>")
        self.indentLevel += 1
        if self.tokenizer.keyWord() != "let":
            raise Exception("Let keyword expected")
        self.printToken() #Should print "let"
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print varname
            varName = self.tokenizer.identifier()
            self.writeVarInfo(self.tokenizer.identifier(), True)
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            print("compileLet - [ or = " + self.tokenizer.currentToken)
            self.printToken() #Should print '[' or '='
        if self.tokenizer.currentToken == "[":
            self.tokenizer.advance()
            self.compileExpression()
            self.printToken() #Should print ']'
            
            if self.symbolTable.isDefined(varName):
                varKind = self.symbolTable.kindOf(varName)
                if varKind == SymbolTable.STATIC:
                    raise Exception("Currently not implemented")
                elif varKind == SymbolTable.FIELD:
                    raise Exception("Currently not implemented")
                elif varKind == SymbolTable.ARGUMENT or varKind == SymbolTable.FIELD:
                    self.vmWriter.writePush(varKind, self.symbolTable.indexOf(varName))

                self.vmWriter.writeArithmetic("add")
                self.vmWriter.writePop("pointer", 1) #Pointer 1 is the segment that points to 'that'
                segment = "that"
                index = 0
            else:
                raise Exception("Symbol " + varName + " is not defined")
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.printToken() #Should print '='
        else:
            #If it goes down this path this is just a regular variable not an array
            varKind = self.symbolTable.kindOf(varName)
            if varKind == SymbolTable.STATIC or varKind == SymbolTable.FIELD:
                raise Exception("Curently not implemented")
            else:
                segment = varKind
                index = self.symbolTable.indexOf(varName)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        print("compileLet - after equals " + self.tokenizer.currentToken)
        self.compileExpression()

        self.vmWriter.writePop(segment, index)
        self.printToken() #print ";"
        
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.indentLevel -= 1
        self.writeFormatted("</letStatement>")

    def compileWhile(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<whileStatement>")
        self.indentLevel += 1

        self.labelNum += 1
        firstLabel = "W" + str(self.labelNum)
        self.labelNum += 1
        secondLabel = "W" + str(self.labelNum)

        if not(self.tokenizer.tokenType == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "while"):
            raise Exception("'while' keyword was expected")
        self.printToken() #print 'while'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #print '('
            self.vmWriter.writeLabel(firstLabel)
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileExpression()
            self.vmWriter.writeArithmetic("not")
            self.vmWriter.writeIf(secondLabel)
            self.printToken() #print ')'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #print '{'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileStatements()
            self.vmWriter.writeGoto(firstLabel)
            self.printToken() #print '}'
            self.vmWriter.writeLabel(secondLabel)
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
        else:
            #When the function's return type is void it should always return 0
            self.vmWriter.writePush("constant", 0)
        self.printToken() #print ";"
        self.vmWriter.writeReturn()
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.indentLevel -= 1
        self.writeFormatted("</returnStatement>")

    def compileIf(self):
        from JackTokenizer import JackTokenizer
        self.writeFormatted("<ifStatement>")
        self.indentLevel += 1
        self.labelNum += 1
        firstLabel = "I" + str(self.labelNum)
        self.labelNum += 1
        secondLabel = "I" + str(self.labelNum)
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
            self.vmWriter.writeArithmetic("not") 
            self.vmWriter.writeIf(firstLabel)
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #print '{'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileStatements()
            self.vmWriter.writeGoto(secondLabel)
            self.vmWriter.writeLabel(firstLabel)
            self.printToken() #print '}'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        if self.tokenizer.tokenType == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "else":
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
        self.vmWriter.writeLabel(secondLabel)
        self.indentLevel -= 1
        self.writeFormatted("</ifStatement>")

    def compileExpression(self):
        from JackTokenizer import JackTokenizer

        #There are 2 symbol arrays which each correspond to a different array with 
        #the commands/functions to call for the given operator in the same index
        functionSymbols = [ '*', '/']
        functionNames = ["Math.multiply", "Math.divide"]
        builtInCommands = ["add", "sub", "and", "or", "lt", "gt", "eq"]
        builtInSymbols = ['+', '-', '&amp;', '|', '&lt;', '&gt;', '=']
        self.writeFormatted("<expression>")
        self.indentLevel += 1
        print("About to call compile term current token is " + self.tokenizer.currentToken)
        self.compileTerm()
        while(self.tokenizer.tokenType == JackTokenizer.SYMBOL and 
                (self.tokenizer.symbol() in builtInSymbols or self.tokenizer.symbol() in functionSymbols)):
            self.printToken()
            operator = self.tokenizer.symbol() 
            print("Current operator " + self.tokenizer.currentToken)
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.compileTerm()

            if operator in builtInSymbols:
                self.vmWriter.writeArithmetic(builtInCommands[builtInSymbols.index(operator)])
            else:
                #Both multiply and divide take two arguments
                self.vmWriter.writeCall(functionNames[functionSymbols.index(operator)], 2)

            
        self.indentLevel -= 1
        self.writeFormatted("</expression>")

    def compileTerm(self):
        from JackTokenizer import JackTokenizer
        print("Opening token is " + self.tokenizer.currentToken)
        unaryOps = ['-', '~']
        unaryCommands = ["neg", "not"]
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

                    self.printToken() #Should print '.'
                    self.tokenizer.advance()
                    self.printToken() #Should print subroutine name
                    subName = self.tokenizer.identifier()

                    self.tokenizer.advance() 
                    self.printToken() #Should print '('

                    self.numExpressions = 0
                    self.tokenizer.advance()
                    self.compileExpressionList()
                    self.printToken() #Should print ')'

                    self.vmWriter.writeCall(name + "." + subName, self.numExpressions)
                    self.tokenizer.advance()
                elif self.tokenizer.symbol() == "(":
                    self.printToken()
                    self.writeClassOrSubInfo("subroutine", True)
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                        self.numExpressions = 0
                        self.compileExpressionList()
                        self.printToken() #Print ')'
                        self.vmWriter.writeCall(name, self.numExpressions)
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                elif self.tokenizer.symbol() == "[":
                    #TODO - IMPLEMENT THIS
                    self.writeVarInfo(name, True)
                    self.printToken()
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                        self.compileExpression()
                        self.printToken() #Should print ']'
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                else:
                    self.vmWriter.writePush(self.symbolTable.kindOf(name), self.symbolTable.indexOf(name))
                    self.writeVarInfo(name, True)
        elif self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == "(":
            self.tokenizer.advance()
            print("second token in (expression)" + self.tokenizer.currentToken)
            self.compileExpression()
            self.printToken() #print ')'
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
        elif self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() in unaryOps:
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            print("second token in unary " + self.tokenizer.currentToken)
            self.compileTerm()
            self.vmWriter.writeArithmetic(unaryCommands[unaryOps.index(op)])
        elif self.tokenizer.tokenType == JackTokenizer.INT_CONST:
            self.vmWriter.writePush("constant", self.tokenizer.intVal())
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
        elif self.tokenizer.currentToken in CompilationEngine.keywordConsts:
            if self.tokenizer.keyWord() == "null" or self.tokenizer.keyWord() == "false":
                self.vmWriter.writePush("constant", 0)
            elif self.tokenizer.keyWord() == "true":
                self.vmWriter.writePush("constant", 1)
                self.vmWriter.writeArithmetic("neg") #Value of true is -1
            elif self.tokenizer.keyWord() == "this":
                raise Exception("Not currently implemented")
            else:
                raise Exception("Invalid keyword constant " + self.tokenizer.keyWord())

            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
        elif self.tokenizer.tokenType == JackTokenizer.STRING_CONST:
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
        self.numExpressions = 0 #The number of expressions in this list

        #I sort of feel guilty for doing this since this relies on knowing that
        #the expression list is surrounded by parenthesis and according to the spec
        #it should not know that (it would require modifying this message if I wanted to use an expression list anywhere else).
        #However, also according to the spec I should create a <subroutineCall> XML element or I shouldn't depending
        #on which part of the spec you trust.
        while not(self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ")"):
           self.compileExpression() 
           self.numExpressions += 1
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
        secondToken = ""
        isClassOrObj = False
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.printToken() #Should print '.' or '(' 
        if self.tokenizer.tokenType == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ".":
            isClassOrObj = True
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance() 
                self.printToken() #Should print subroutine name
                secondToken = self.tokenizer.currentToken
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                self.printToken() #Should print opening '('
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileExpressionList()
            self.printToken() #Should print ')'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

        
        callName = firstToken 
        if secondToken != "":
            callName += "." + secondToken

        self.vmWriter.writeCall(callName, self.numExpressions) 

        if isClassOrObj and self.symbolTable.isDefined(firstToken):
            self.writeVarInfo(classToken, True) #Writing information about an object
        elif isClassOrObj:
            self.writeClassOrSubInfo("class", True) #Writing information about a class
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
