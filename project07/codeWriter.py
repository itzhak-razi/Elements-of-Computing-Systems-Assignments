class CodeWriter:

    def __init__(self, fileOut):
        self.outputFile = fileOut
        self.labelCounter = 0

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
            self.outputFile.write("M=M-D\n") 
        elif command == "neg":
            self.outputFile.write("@SP\n")
            self.outputFile.write("A=M-1\n")
            self.outputFile.write("M=-M\n")
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
            label = "negate" + str(self.labelCounter)
            self.labelCounter += 1
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
            self.greaterThanLessThanJump("JLT")
        elif command == "gt":
            self.greaterThanLessThanJump("JGT")
            

    def writePushPop(self, command, segment, index):
        import stackParser
        from stackParser import Parser 
        if command == Parser.C_PUSH:
            if segment == "constant":
                self.outputFile.write("@" + str(index) + "\n")
                self.outputFile.write("D=A\n")
                self.push()
            if segment == "argument":
                self.pushFromRAM("ARG", index)
            if segment == "local":
                self.pushFromRAM("LCL", index)
            if segment == "this":
                self.pushFromRAM("THIS", index)
            if segment == "that":
                self.pushFromRAM("THAT", index)
            if segment == "temp":
                self.outputFile.write("@5\n")
                self.outputFile.write("D=A\n")
                self.outputFile.write("@" + index + "\n")
                self.outputFile.write("A=D+A\n")
                self.outputFile.write("D=M\n")
                self.push()
        if command == Parser.C_POP:
            if segment == "argument":
                self.storeToRAM("ARG", index)
            if segment == "local":
                self.storeToRAM("LCL", index)
            if segment == "this":
                self.storeToRAM("THIS", index)
            if segment == "that":
                self.storeToRAM("THAT", index)
            if segment == "temp":
                self.outputFile.write("@5\n")
                self.outputFile.write("D=A\n")
                self.outputFile.write("@13\n") #13 being a temp register
                self.outputFile.write("M=D\n")
                self.outputFile.write("@" + index + "\n")
                self.outputFile.write("D=A\n")
                self.outputFile.write("@13\n")
                self.outputFile.write("M=M+D\n")
                self.outputFile.write("@SP\n")
                self.outputFile.write("M=M-1\n")
                self.outputFile.write("A=M\n")
                self.outputFile.write("D=M\n")
                self.outputFile.write("@13\n")
                self.outputFile.write("A=M\n")
                self.outputFile.write("M=D\n")
    
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
    
    def pushFromRAM(self, segmentVar, index):
        self.outputFile.write("@" + segmentVar + "\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@" + index + "\n")
        self.outputFile.write("A=D+A\n")
        self.outputFile.write("D=M\n")
        self.push()

    def storeToRAM(self, segmentVar, index):
        self.outputFile.write("@" + segmentVar + "\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@13\n") #13 being a temp register
        self.outputFile.write("M=D\n")
        self.outputFile.write("@" + index + "\n")
        self.outputFile.write("D=A\n")
        self.outputFile.write("@13\n")
        self.outputFile.write("M=M+D\n")
        self.outputFile.write("@SP\n")
        self.outputFile.write("M=M-1\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@13\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("M=D\n")
        
    def greaterThanLessThanJump(self, jumpCmd):
        negateLbl = "negate" + str(self.labelCounter)
        setTrueLbl = "setTrue" + str(self.labelCounter)
        self.labelCounter += 1
        self.pop()
        self.outputFile.write("@SP\n")
        self.outputFile.write("A=M-1\n")
        self.outputFile.write("D=M-D\n")
        self.outputFile.write("@" + setTrueLbl + "\n")
        self.outputFile.write("D;" + jumpCmd + "\n")
        self.outputFile.write("D=0\n")
        self.outputFile.write("D=!D\n")
        self.outputFile.write("@" + negateLbl + "\n")
        self.outputFile.write("0;JMP\n")
        self.outputFile.write("(" + setTrueLbl + ")\n")
        self.outputFile.write("D=0\n")
        self.outputFile.write("(" + negateLbl + ")\n")
        self.outputFile.write("@SP\n")
        self.outputFile.write("A=M-1\n")
        self.outputFile.write("M=!D\n")

    def close(self):
        self.outputFile.close()
