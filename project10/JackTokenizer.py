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
       while currentIndex < len(fileContents):
           index = fileContents.find("\"", currentIndex)
           if index < fileContents.find("/"):
               currentIndex = fileContents.find("\"", index + 1)
           else:
               currentIndex = fileContents.find("/")
            
           if currentIndex + 1 == "*":



    def hasMoreTokens(self):
        pass
    def advance(self):
    def tokenType(self):
    def keyWord(self):
    def symbol(self):
    def identifier(self):
    def intVal(self):
    def stringVal(self):
