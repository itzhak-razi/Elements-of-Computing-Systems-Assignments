class CodeWriter:

    def __init__(self, fileOut):
        self.outputFile = fileOut
        self.negateCounter = 0

    def setFileName(self, fileName):
        self.currentName = fileName

    def writeArithmetic(self, command):
        if command == "add":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M-1\n")
            self.outputFile.write("M=M+D\n")
        elif command == "sub":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M-1\n")
            self.outputFile.write("M=M-D\n") #Should it be M-D?
        elif command == "neg":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M\n")
            self.outputFile.write("M=-D\n")
        elif command == "and":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M-1\n")
            self.outputFile.write("M=M & D\n")
        elif command == "or":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M-1\n")
            self.outputFile.write("M=M | D\n")
        elif command == "not":
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M\n")
            self.outputFile.write("M=!D")
        elif command == "eq":
            label = "negate" + str(negateCounter)
            self.pop()
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M-1\n")
            self.outputFile.write("D=M-D\n") #or D-M, doesn't matter
            self.outputFile.write("@" + label + "\n")
            self.outputFile.write("D;JEQ\n")
            self.outputFile.write("D=1\n")
            self.outputFile.write("(" + label + ")\n")
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M-1\n")
            self.outputFile.write("M=!D\n")
        elif command == "lt":
            self.outputFile.write("//TODO")
        elif command == "gt":
            self.outputFile.write("//TODO")
            

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
