class CodeWriter:

    def __init__(self, fileOut):
        self.outputFile = fileOut
        self.outputFile.write("@255")
        self.outputFile.write("D=A")
        self.outputFile.write("@SP")
        self.outputFile.write("M=D")

    def setFileName(self, fileName):
        self.currentName = fileName

    def writeArithmetic(self, command):
        if command == "add":
            pop(self)
            self.outputFile.write("@SP")
            self.outputFile.write("M=M+D")
        elif command == "sub":
            pop(self)
            self.outputFile.write("@SP")
            self.outputFile.write("M=D-M")
        elif command == "neg":
            self.outputFile.write("@SP")
            self.outputFile.write("M=-M")
        elif command == "eq":
            pop(self)
            self.outputFile.write("@SP")
            self.outputFile
            

    def writePushPop(self, command, segment, index):
        import stackParser
        from stackParser import Parser 
        if command == Parser.C_PUSH:
            if segment == "constant":
                self.outputFile.write("@" + str(index))
                self.outputFile.write("D=A")
                push(self)
    
    #Pushes the value in D into the stack
    def push(self):
        self.outputFile.write("@SP")
        self.outputFile.write("M=M+1")
        self.outputFile.write("A=M")
        self.outputFile.write("M=D")

    #Pops the stack and puts the value into the D register
    def pop(self):
        self.outputFile.write("@SP")
        self.outputFile.write("D=M")
        self.outputFile.write("M=M-1")

    def close(self):
        self.outputFile.close()
