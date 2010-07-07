def translate(fileName):
    import codeWriter
    from codeWriter import CodeWriter
    import stackParser
    from stackParser import Parser
    import os
   
    files = [] 
    ext = os.path.splitext(fileName)[1]


    if ext == '':
        outputFile = open(os.path.join(fileName, os.path.basename(os.path.abspath(fileName)) + ".asm"), 'w')
        for currentFile in os.listdir(fileName):
            if os.path.splitext(currentFile)[1] == '.vm':
                files.append(os.path.join(fileName, currentFile))
    elif ext == '.vm':
        outputFile = open(os.path.splitext(fileName)[0] + ".asm", 'w')
        files.append(fileName)
    else:
        raise Exception("File provided doesn't have a .vm extension and is not a directory")

    
    codeWriter = CodeWriter(outputFile)
    for file in files:
        file = open(file, 'r')
        parser = Parser(file)
        parse(parser, codeWriter, file)
    codeWriter.close() 


def parse(parser, codeWriter, fileName):
    import stackParser
    from stackParser import Parser
    codeWriter.setFileName(fileName)
    while parser.hasMoreCommands():
        parser.advance()
        print("Type is " + str(parser.commandType()) + " and command is " + parser.current())
        if parser.commandType() == Parser.C_ARITHMETIC:
            codeWriter.writeArithmetic(parser.arg1())
        elif (parser.commandType() == Parser.C_PUSH) | (parser.commandType() == Parser.C_POP):
            codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())
        else:
            print("Well here we are")

