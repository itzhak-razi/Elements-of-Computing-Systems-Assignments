def translate(fileName):
    import codeWriter
    from codeWriter import CodeWriter
    import stackParser
    from stackParser import Parser
    import os
   
    files = [] 
    ext = os.path.splitext(fileName)[1]


    if ext == '':
        for currentFile in os.listdir(fileName):
            if os.path.splitext(currentFile)[1] == '.vm':
                files.append(currentFile)
    elif ext == '.vm':
        files.append(fileName)
    else:
        raise Exception("File provided doesn't have a .vm extension and is not a directory")

    
    outputFile = open(os.path.splitext(fileName)[0] + ".asm", 'w')
    codeWriter = CodeWriter(outputFile)
    for fileName in files:
        file = open(fileName, 'r')
        parser = Parser(file)
        parse(parser, codeWriter, fileName)
    codeWriter.close() 


def parse(parser, codeWriter, fileName):
    import stackParser
    from stackParser import Parser
    codeWriter.setFileName(fileName)
    while parser.hasMoreCommands():
        parser.advance()
        if parser.commandType() == Parser.C_ARITHMETIC:
            codeWriter.writeArithmetic(parser.arg1())
        elif parser.commandType() == Parser.C_PUSH | parser.commandType() == Parser.C_POP:
            codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())

