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
    
       print("With comments removed\n\n" + commentsRemoved)


           
    

    def hasMoreTokens(self):
        pass
    def advance(self):
        pass
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
