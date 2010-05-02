def assemble(fileName):
    import assemblerParser
    from assemblerParser import Parser
    import code
    file=open(fileName, 'r')
    outputFile = open(fileName[:fileName.find(".")] + ".hack", 'w')
    parser = Parser(file)
    while parser.hasMoreCommands():
        if(parser.commandType() == Parser.C_COMMAND):
            output = "111" + code.comp(parser.comp()) + code.dest(parser.dest()) + code.jump(parser.jump())
            outputFile.write(output)
        elif parser.commandType() == Parser.A_COMMAND:
            binVal=bin(parser.symbol())[2:]
            output = "0" * (16-len(binVal)) + binVal
            outputFile.write(output)
        parser.advance()
