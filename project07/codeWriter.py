class CodeWriter:

    def __init__(self, fileOut):
        self.outputFile = fileOut

    def setFileName(self, fileName):
        self.currentName = fileName

    def writeArithmetic(self, command):
        
    def writePushPop(self, command, segment, index):
        import stackParser
        from stackParser import Parser 
        if command == Parser.C_PUSH:
            if segment == "constant":
                self.outputFile.write("@" + str(index))
                self.outputFile.write("M=" + D)

    def close(self):
        self.outputFile.close()
