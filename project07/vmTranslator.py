def translate(fileName):
    import codeWriter
    from codeWriter import CodeWriter
    import stackParser
    from stackParser import Parser
    import os
   
    files = [] 
    outputFile = open(os.path.splitext(fileName)[0], 'w')
    ext = os.path.splitext(fileName)[1]

    codeWriter = CodeWriter(outputFile)

    if ext == '':
        for currentFile in os.listdir(fileName):
            if os.path.splitext(currentFile)[1] == '.vm':
                files.append(currentFile)
    elif ext == '.vm':
        files.append(fileName)
    else:
        raise Exception("File provided doesn't have a .vm extension and is not a directory")

    
    for fileName in files:
        file = open(fileName, 'r')
        parser = Parser(file)
        parse(parser, codeWriter)
         
def parse(parser, codeWriter):
    while parser.hasMoreCommands():
        parser.advance()
