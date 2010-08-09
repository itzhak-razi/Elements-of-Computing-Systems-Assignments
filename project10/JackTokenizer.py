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
                commentsRemoved += fileContents[currentIndex]
                currentIndex += 1
            elif (not quoteMode) and fileContents[currentIndex] == "/" and fileContents[currentIndex + 1] == "/": 
                currentIndex = fileContents.find("\n", currentIndex + 1)
            elif (not quoteMode) and fileContents[currentIndex] == "/" and fileContents[currentIndex + 1] == "*":
                currentIndex = fileContents.find("*/", currentIndex + 1) + 2
            else:
                commentsRemoved += fileContents[currentIndex]
                currentIndex += 1
        self.commentsRemoved += fileContents[currentIndex]
        
       

    def hasMoreTokens(self):
        import re
        if re.search("[^ ]", self.commentsRemoved[self.tokenIndex + 1 : ])
            return True
        return False

    def advance(self):
        import re
        #strip spaces
        while self.tokenIndex < len(self.commentsRemoved) and 
              self.commentsRemoved[self.tokenIndex].isspace():
            self.tokenIndex = self.tokenIndex + 1
        #match keywords
        if self.commentsRemoved[self.tokenIndex].isalpha():
            for currentKeyword in KEYWORDS:
                if re.match(currentKeyword, self.commentsRemoved[self.tokenIndex:]):
                    self.currentToken = currentKeyword
                    self.tokenIndex += len(currentKeyword)
                    self.tokenType = JackTokenizer.KEYWORD
                    break
        #match string constants 
        elif self.commentsRemoved[self.tokenIndex] == "\"":
            quoteGroup = re.match("\"[^\"]*\"", self.commentsRemoved[self.tokenIndex:]
            self.currentToken = quoteGroup.group(0)
            self.tokenIndex += len(self.currentToken)
            self.tokenType = JackTokenizer.STRING_CONST
        #match symbols
        elif not self.commentsRemoved[self.tokenIndex].isnumeric():
            for currentSymbol in SYMBOLS:
                if re.match(currentSymbol, self.commentsRemoved(self.tokenIndex]):
                    self.tokenIndex += 1
                    self.tokenType = JackTokenizer.SYMBOL
        #match integer constants
        elif self.commentsRemoved[self.tokenIndex].isnumeric():
            numGroup = re.match("\d+", self.commentsRemoved[self.tokenIndex:])
            self.currentToken = numGroup.group(0)
            self.tokenIndex += len(self.currentToken)
            self.tokenType = JackTokenizer.INT_CONST
        #match identifier
        else:
            identifierMatch = re.match("[a-zA-Z_]+[a-ZA-Z0-9_]*", self.commentsRemoved[self.tokenIndex:]
            self.currentToken = identifierMatch.group(0)
            self.tokenIndex += len(self.currentToken)
            self.tokenType = JackTokenizer.IDENTIFIER

    def tokenType(self):
        return self.tokenType

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
