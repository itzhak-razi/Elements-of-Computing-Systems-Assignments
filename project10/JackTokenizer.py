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
            print("Attempting alpha match")
            for currentKeyword in JackTokenizer.KEYWORDS:
                if re.match(currentKeyword, self.commentsRemoved[self.tokenIndex:]):
                    self.currentToken = currentKeyword
                    self.tokenIndex += len(currentKeyword)
                    self.type = JackTokenizer.KEYWORD
                    matched = True
                    break
        #match string constants 
        if self.commentsRemoved[self.tokenIndex] == "\"" and not matched:
            print("Attempting str constants match")
            quoteGroup = re.match("\"[^\"]*\"", self.commentsRemoved[self.tokenIndex:])
            self.currentToken = quoteGroup.group(0)
            self.tokenIndex += len(self.currentToken)
            self.type = JackTokenizer.STRING_CONST
            matched = True
        #match symbols
        if (not self.commentsRemoved[self.tokenIndex].isdigit()) and (not matched):
            print("Attempting symbols match")
            for currentSymbol in JackTokenizer.SYMBOLS:
                if currentSymbol == self.commentsRemoved[self.tokenIndex]:
                    self.tokenIndex += 1
                    self.type = JackTokenizer.SYMBOL
                    self.currentToken = currentSymbol
                    matched = True
        #match integer constants
        if self.commentsRemoved[self.tokenIndex].isdigit() and not matched:
            print("Attempting int constants match")
            numGroup = re.match("\d+", self.commentsRemoved[self.tokenIndex:])
            self.currentToken = numGroup.group(0)
            self.tokenIndex += len(self.currentToken)
            self.type = JackTokenizer.INT_CONST
            matched = True
        #match identifier
        if not matched:
            print("Attempting identifier match")
            identifierMatch = re.match("[a-zA-Z_]+[a-zA-Z0-9_]*", self.commentsRemoved[self.tokenIndex:])
            self.currentToken = identifierMatch.group(0)
            self.tokenIndex += len(self.currentToken)
            self.type = JackTokenizer.IDENTIFIER

    def tokenType(self):
        return self.type

    def keyWord(self):
        return self.currentToken

    def symbol(self):
        return self.currentToken

    def identifier(self):
        return self.currentToken

    def intVal(self):
        return self.currentToken

    def stringVal(self):
        return self.currentToken[1:len(self.currentToken) - 2] #strips the quotes 

    def current(self):
        return self.currentToken
