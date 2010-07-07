class CodeWriter:

    def __init__(self, fileOut):
        self.outputFile = fileOut
        """ 
        #Initialization code
        self.outputFile.write("@255\n")
        self.outputFile.write("D=A\n")
        self.outputFile.write("@SP\n")
        self.outputFile.write("M=D\n")
        """

    def setFileName(self, fileName):
        self.currentName = fileName

    def writeArithmetic(self, command):
        if command == "add":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("M=M+D\n")
        elif command == "sub":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("M=D-M\n")
        elif command == "neg":
            self.outputFile.write("@SP\n")
            self.outputFile.write("M=-M\n")
        elif command == "eq":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile
            

    def writePushPop(self, command, segment, index):
        import stackParser
        from stackParser import Parser 
        if command == Parser.C_PUSH:
            if segment == "constant":
                self.outputFile.write("@" + str(index) + "\n")
                self.outputFile.write("D=A\n")
                self.push()
    
    #Pushes the value in D into the stack
    def push(self):
        self.outputFile.write("@SP\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("M=D\n")
        self.outputFile.write("@SP\n")
        self.outputFile.write("M=M+1\n")

    #Pops the stack and puts the value into the D register
    def pop(self):
        self.outputFile.write("@SP\n")
        self.outputFile.write("M=M-1\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("D=M\n")

    def close(self):
        self.outputFile.close()
