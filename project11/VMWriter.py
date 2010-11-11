class VMWriter:

    def __init__(self, outputFile):
        self.outputFile = outputFile

    def writePush(self, segment, index):
        self.outputFile.write("push " + segment + " " + str(index) + "\n")

    def writePop(self, segment, index):
        self.outputFile.write("pop " + segment + " " + str(index) + "\n")

    def writeArithmetic(self, command):
        self.outputFile.write(command + "\n")

    def writeLabel(self, label):
        self.outputFile.write("label " + label + "\n")

    def writeGoto(self, label):
        self.outputFile.write("goto " + label + "\n")

    def writeIf(self, label):
        self.outputFile.write("if-goto " + label + "\n")

    def writeCall(self, name, nArgs):
        self.outputFile.write("call " + name + " " + str(nArgs) + "\n")

    def writeFunction(self, name, nLocals):
        self.outputFile.write("function " + name + " " + str(nLocals) + "\n")

    def writeReturn(self):
        self.outputFile.write("return\n")
