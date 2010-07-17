class CodeWriter:

    def __init__(self, fileOut):
        self.outputFile = fileOut
        self.labelCounter = 0
        self.currentFunction = ""
        self.returnNum = 0

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
            elif segment == "static":
                self.outputFile.write("@" + self.currentName + "." + str(index) + "\n")
                self.outputFile.write("D=M\n")
                self.push()
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
            elif segment == "static":
                self.pop()
                self.outputFile.write("@" + self.currentName + "." + str(index) + "\n")
                self.outputFile.write("M=D\n")
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

    def writeLabel(self, label):
        self.outputFile.write("(" + self.labelName(label) + ")\n")

    def writeGoto(self, label):
        self.outputFile.write("@" + self.labelName(label) + "\n")
        self.outputFile.write("0;JMP\n")

    def writeIf(self, label):
        self.pop()
        self.outputFile.write("@" + self.labelName(label) + "\n")
        self.outputFile.write("D;JNE\n")

    def writeInit(self):
        self.outputFile.write("@256\n")
        self.outputFile.write("D=A\n")
        self.outputFile.write("@SP\n")  
        self.outputFile.write("M=D\n")
        self.writeCall("Sys.init", 0)

    def writeCall(self, functionName, numArgs):
        self.outputFile.write("@return" + self.currentFunction + str(self.returnNum) + "\n")
        self.outputFile.write("D=A\n")
        self.push()
        self.outputFile.write("@LCL\n")
        self.outputFile.write("D=M\n")
        self.push()
        self.outputFile.write("@ARG\n")
        self.outputFile.write("D=M\n")
        self.push()
        self.outputFile.write("@THIS\n")
        self.outputFile.write("D=M\n")
        self.push()
        self.outputFile.write("@THAT\n")
        self.outputFile.write("D=M\n")
        self.push()
        self.outputFile.write("@SP\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@ARG\n")
        self.outputFile.write("M=D\n")
        self.outputFile.write("@" + str(numArgs) + "\n")
        self.outputFile.write("D=A\n")
        self.outputFile.write("@ARG\n")
        self.outputFile.write("M=M-D\n")
        self.outputFile.write("@5\n")
        self.outputFile.write("D=A\n")
        self.outputFile.write("@ARG\n")
        self.outputFile.write("M=M-D\n")
        self.outputFile.write("@SP\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@LCL\n")
        self.outputFile.write("@" + functionName + "\n")
        self.outputFile.write("0;JMP\n")
        self.outputFile.write("(return" + self.currentFunction + str(self.returnNum) + ")\n")


    def writeFunction(self, functionName, numLocals):
        self.currentFunction = functionName
        self.returnNum = 0
        self.outputFile.write("(" + functionName +")\n")
        self.outputFile.write("@R13\n")
        self.outputFile.write("M=0\n")
        self.outputFile.write("(" + functionName +"loopStart)\n")
        self.outputFile.write("@" + str(numLocals) + "\n")
        self.outputFile.write("D=A\n")
        self.outputFile.write("@R13\n")
        self.outputFile.write("D=A-M\n")
        self.outputFile.write("@" + functionName + "loopEnd\n")
        self.outputFile.write("D;JLE\n")
        #push 0
        self.outputFile.write("@SP\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("M=0\n")
        self.outputFile.write("@SP\n")
        self.outputFile.write("M=M+1\n")
        #increment counter and goto start of loop
        self.outputFile.write("@R13\n")
        self.outputFile.write("M=M+1\n")
        self.outputFile.write("@" + functionName + "loopStart\n")
        self.outputFile.write("0;JMP\n")
        self.outputFile.write("(" + functionName + "loopEnd)\n")



    def writeReturn(self):
        self.currentFunction = ""
        self.outputFile.write("@LCL\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@R13\n") #R13 = FRAME
        self.outputFile.write("M=D\n")
        self.outputFile.write("@R14\n") #R14 = RET
        self.outputFile.write("M=D\n")
        self.outputFile.write("@5\n")
        self.outputFile.write("D=A\n")
        self.outputFile.write("@R14\n")
        self.outputFile.write("M=M-D\n")
        self.pop()
        self.outputFile.write("@ARG\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("M=D\n")
        self.outputFile.write("@ARG\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@SP\n")
        self.outputFile.write("M=D+1\n")
        self.outputFile.write("@R13")
        self.outputFile.write("M=M-1\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@THAT\n")
        self.outputFile.write("M=D\n")
        self.outputFile.write("@R13\n")
        self.outputFile.write("M=M-1\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@THIS\n")
        self.outputFile.write("M=D\n")
        self.outputFile.write("@R13\n")
        self.outputFile.write("M=M-1\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@ARG\n")
        self.outputFile.write("M=D\n")
        self.outputFile.write("@R13\n")
        self.outputFile.write("M=M-1\n")
        self.outputFile.write("A=M\n")
        self.outputFile.write("D=M\n")
        self.outputFile.write("@LCL\n")
        self.outputFile.write("M=D\n")
        self.outputFile.write("@R14\n")
        self.outputFile.write("0;JMP\n")

    def labelName(self, label):
        return self.currentFunction + "$" + label

