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
            elif segment == "argument":
                self.preambleLocationInMemory("ARG")
                self.pushFromRAM(index)
            elif segment == "local":
                self.preambleLocationInMemory("LCL")
                self.pushFromRAM(index)
            elif segment == "this":
                self.preambleLocationInMemory("THIS")
                self.pushFromRAM(index)
            elif segment == "that":
                self.preambleLocationInMemory("THAT")
                self.pushFromRAM(index)
            elif segment == "temp":
                self.preambleLocationIsMemory("5")
                self.pushFromRAM(index)
            elif segment == "pointer":
                self.preambleLocationIsMemory("3")
                self.pushFromRAM(index)
            else:
                print("ERROR: segment undefined, segment given - " + segment)
        elif command == Parser.C_POP:
            if segment == "argument":
                self.preambleLocationInMemory("ARG")
                self.storeToRAM(index)
            elif segment == "local":
                self.preambleLocationInMemory("LCL")
                self.storeToRAM(index)
            elif segment == "this":
                self.preambleLocationInMemory("THIS")
                self.storeToRAM(index)
            elif segment == "that":
                self.preambleLocationInMemory("THAT")
                self.storeToRAM(index)
            elif segment == "temp":
                self.preambleLocationIsMemory("5")
                self.storeToRAM(index)
            elif segment == "pointer":
                self.preambleLocationIsMemory("3")
                self.storeToRAM(index)
            else:
                print("ERROR: segment undefined, segment given - " + segment)

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
    
    def pushFromRAM(self, index):
        self.outputFile.write("@" + index + "\n")
        self.outputFile.write("A=D+A\n")
        self.outputFile.write("D=M\n")
        self.push()

    def preambleLocationInMemory(self, segmentVar):
        self.outputFile.write("@" + segmentVar + "\n")
        self.outputFile.write("D=M\n")

    def preambleLocationIsMemory(self, memoryLoc):
        self.outputFile.write("@" + str(memoryLoc) + "\n")
        self.outputFile.write("D=A\n")

    #Pops stack and puts it into a memory location index spaces away from the memory
    #location currently in D.  premableLocationIsMemory() or preambleLocationInMemory()
    #may be called to set up the D value.
    def storeToRAM(self, index):
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
