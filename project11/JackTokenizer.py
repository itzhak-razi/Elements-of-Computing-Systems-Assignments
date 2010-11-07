class JackTokenizer:

    KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int",
                "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if",
                "else", "while", "return"]

    SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<',
                '>', '=', '~']    
    
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4

    def __init__(self, inputFile):
        import re
        fileContents = inputFile.read()
        currentIndex = 0
        quoteMode = False
        self.commentsRemoved = ""
        self.currentToken = ""
        self.tokenIndex = 0

        #Loop to strip comments.  Note that if a file has a beginning comment indicator (// or /*) 
        #as the last characters this won't remove them.
        while currentIndex < len(fileContents) - 1:
            if fileContents[currentIndex] == "\"":
                quoteMode = not quoteMode
                self.commentsRemoved += fileContents[currentIndex]
                currentIndex += 1
            elif (not quoteMode) and fileContents[currentIndex] == "/" and fileContents[currentIndex + 1] == "/": 
                currentIndex = fileContents.find("\n", currentIndex + 1)
            elif (not quoteMode) and fileContents[currentIndex] == "/" and fileContents[currentIndex + 1] == "*":
                currentIndex = fileContents.find("*/", currentIndex + 1) + 2
            else:
                self.commentsRemoved += fileContents[currentIndex]
                currentIndex += 1
        self.commentsRemoved += fileContents[currentIndex]
        
       

    def hasMoreTokens(self):
        import re
        if re.search("[^ ]", self.commentsRemoved[self.tokenIndex + 1 : ]):
            return True
        return False

    def advance(self):
        import re
        matched = False
        #strip spaces
        while(self.tokenIndex < len(self.commentsRemoved) and 
              self.commentsRemoved[self.tokenIndex].isspace()):
            self.tokenIndex += 1

        if not self.tokenIndex < len(self.commentsRemoved):
            return

        #match keywords
        if self.commentsRemoved[self.tokenIndex].isalpha():
            for currentKeyword in JackTokenizer.KEYWORDS:
                if re.match(currentKeyword, self.commentsRemoved[self.tokenIndex:]):
                    self.currentToken = currentKeyword
                    self.tokenIndex += len(currentKeyword)
                    self.tokenType = JackTokenizer.KEYWORD
                    matched = True
                    break
        #match string constants 
        if not matched and self.commentsRemoved[self.tokenIndex] == "\"":
            quoteGroup = re.match("\"[^\"]*\"", self.commentsRemoved[self.tokenIndex:])
            self.currentToken = quoteGroup.group(0)
            self.tokenIndex += len(self.currentToken)
            self.tokenType = JackTokenizer.STRING_CONST
            matched = True
        #match symbols
        if (not matched) and (not self.commentsRemoved[self.tokenIndex].isdigit()):
            for currentSymbol in JackTokenizer.SYMBOLS:
                if currentSymbol == self.commentsRemoved[self.tokenIndex]:
                    self.tokenIndex += 1
                    self.tokenType = JackTokenizer.SYMBOL
                    self.currentToken = currentSymbol
                    matched = True
                    break
        #match integer constants
        if not matched and self.commentsRemoved[self.tokenIndex].isdigit():
            numGroup = re.match("\d+", self.commentsRemoved[self.tokenIndex:])
            self.currentToken = numGroup.group(0)
            self.tokenIndex += len(self.currentToken)
            self.tokenType = JackTokenizer.INT_CONST
            matched = True
        #match identifier
        if not matched:
            identifierMatch = re.match("[a-zA-Z_]+[a-zA-Z0-9_]*", self.commentsRemoved[self.tokenIndex:])
            self.currentToken = identifierMatch.group(0)
            self.tokenIndex += len(self.currentToken)
            self.tokenType = JackTokenizer.IDENTIFIER

    def keyWord(self):
        if self.tokenType != JackTokenizer.KEYWORD:
            raise TypeError("Keyword token not available")
        return self.currentToken

    def symbol(self):
        if self.tokenType != JackTokenizer.SYMBOL:
            raise TypeError("Symbol token not available - token is " + self.currentToken)
        if self.currentToken == "<":
            return "&lt;"
        elif self.currentToken == ">":
            return "&gt;"
        elif self.currentToken == "&":
            return "&amp;"
        elif self.currentToken == '"':
            return "&quot;"
        else:
            return self.currentToken

    def identifier(self):
        if self.tokenType != JackTokenizer.IDENTIFIER:
            raise TypeError("Identifier token not available - token is " + self.currentToken)
        return self.currentToken

    def intVal(self):
        if self.tokenType != JackTokenizer.INT_CONST:
            raise TypeError("Integer token not available - token is " + self.currentToken)
        return self.currentToken

    def stringVal(self):
        if self.tokenType != JackTokenizer.STRING_CONST:
            raise TypeError("String token not available - token is " + self.currentToken)
        return self.currentToken[1:len(self.currentToken) - 2] #strips the quotes 
