def assemble(fileName):
    import assemblerParser
    from assemblerParser import Parser
    import code
    num = bin(128)
    print("The number in binary is " + str(num))
    print("The fileName is " + fileName)
    file = open(fileName, 'r')
    newFileName = fileName[:fileName.find(".", 1)] + ".hack"
    print("The new file is " + newFileName)
    outputFile = open(newFileName, 'w')
    parser = Parser(file)
    while parser.hasMoreCommands():
        parser.advance()
        output = "BLANK"
        if(parser.commandType() == Parser.C_COMMAND):
            output = "111" + code.comp(parser.comp()) + code.dest(parser.dest()) + code.jump(parser.jump())
            outputFile.write(output)
        elif parser.commandType() == Parser.A_COMMAND:
            binVal=bin(int(parser.symbol()))[2:]
            output = "0" * (16-len(binVal)) + binVal
            outputFile.write(output)
        outputFile.write("\n")
        print(parser.current() + " " + "BIN: " + output)
