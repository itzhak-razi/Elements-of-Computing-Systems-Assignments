class JackTokenizer:

    KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int",
                "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if",
                "else", "while", "return"]

    SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<',
                '>', '=', '~']    

    


    def __init__(self, inputFile):
       import re
       fileContents = inputFile.read()
       currentIndex = 0
       commentsRemoved = ""
       quoteMode = False
       self.currentToken = ""

       #Loop to strip comments
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
       commentsRemoved += fileContents[currentIndex]
        
       self.spaceSplit = re.split("\s+", commentsRemoved)


    def hasMoreTokens(self):
        if len(self.spaceSplit) > 0:
            return True
        return False 

    def advance(self):
        self.currentToken = self.spaceSplit.pop(0)
        for currentSymbol in SYMBOLS:
            if(re.match(currentSymbol, self.currentToken) and 
               len(currentSymbol) < len(self.currentToken)):
                self.spaceSplit.insert(0, self.currentToken[len(currentSymbol):])
                self.currentToken = currentSymbol

        for currentKeyword in KEYWORDS:
            if(re.match(currentKeyword, self.currentToken) and
               len(currentKeyword) < len(self.currentToken)):
                self.spaceSplit.insert(0, self.currentToken[len(currentKeyword):])
                self.currentToken = currentKeyword 



    def tokenType(self):
        pass

    def keyWord(self):
        pass

    def symbol(self):
        pass

    def identifier(self):
        pass

    def intVal(self):
        pass

    def stringVal(self):
        pass

    def current(self):
        return self.currentToken
