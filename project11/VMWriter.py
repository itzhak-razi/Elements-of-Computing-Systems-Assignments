class VMWriter:

    def __init__(self, outputFile):
        self.outputFile = outputFile

    def writePush(self, segment, index):
        self.outputFile.write("push " + segment + " " + index + "\n")

    def writePop(self, segment, index):
        self.outputFile.write("pop " + segment + " " + index + "\n")

    def writeArithmetic(self, command):
        self.outputFile.write(command + "\n")

    def writeLabel(self, label):
        self.outputFile.write("label " + label + "\n")

    def writeGoto(self, label):
        self.outputFile.write("goto " + label "\n")

    def writeIf(self, label):
        self.outputFile.write("if-goto " + label + "\n")

    def writeCall(self, name, nArgs):
        self.outputFile.write("call " + name + " " + nArgs + "\n")

    def writeFunction(self, name, nLocals):
        self.outputFile.write("function " + name + " " + nLocals + "\n")

    def writeReturn(self):
        self.outputFile.write("return\n")
