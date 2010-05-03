def assemble(fileName):
    import assemblerParser
    from assemblerParser import Parser
    import code
    import symbolTable
    from symbolTable import SymbolTable

    WORD_SIZE = 16 #words are 16 bits long
    currentDataAddr = 16
    file = open(fileName, 'r')
    parser = Parser(file)
    
    table = SymbolTable()
    #Symbol generating pass
    counter = 0
    while(parser.hasMoreCommands()):
        parser.advance()
        if(parser.commandType() == Parser.L_COMMAND):
            table.addEntry(parser.symbol(), counter)
        else:
            counter += 1


    newFileName = fileName[:fileName.find(".", 1)] + ".hack"
    outputFile = open(newFileName, 'w')
    #Code generating pass
    file = open(fileName, 'r')
    parser = Parser(file)
    while parser.hasMoreCommands():
        parser.advance()
        output = "BLANK"
        if(parser.commandType() == Parser.C_COMMAND):
            output = "111" + code.comp(parser.comp()) + code.dest(parser.dest()) + code.jump(parser.jump())
            outputFile.write(output + "\n")
        elif parser.commandType() == Parser.A_COMMAND:
            symbol = parser.symbol()
            try:
                symbol = int(symbol)
            except:
                pass

            if type(symbol) is int:
                binVal=bin(int(symbol))[2:] #the slice is because the value will be in the form 0b# so we need to remove the 0b
            elif table.contains(symbol):
                binVal = bin(table.getAddress(symbol))[2:]
            else:
                table.addEntry(symbol, currentDataAddr)
                binVal = bin(currentDataAddr)[2:]
                currentDataAddr += 1
            output = "0" * (WORD_SIZE - len(binVal)) + binVal
            outputFile.write(output + "\n")
        elif parser.commandType() == Parser.L_COMMAND:
            pass
        else:
            print("Bad Munkey!")
        print("Original is " + parser.current() + " BIN: " + output + "COMP: " + parser.comp())
