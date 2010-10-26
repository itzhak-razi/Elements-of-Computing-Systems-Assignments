class JackAnalyzer:

    def __init__(self, input):
        import os
        from JackTokenizer import JackTokenizer
        

        files = []
        dir = os.path.splitext(input)[0]
        ext = os.path.splitext(input)[1]

        if ext == '':
            for currentFile in os.listdir(input):
                if os.path.splitext(currentFile)[1] == '.jack':
                    files.append(os.path.join(input, currentFile))
        elif ext == '.jack':
            #os.path.splitext will only return the directory when the file doesn't have an extension
            dir = os.path.split(input)[0] 
            files.append(input)
        else: 
            raise Exception("File provided doesn't have a .jack extension")
    
        for fileName in files:
            self.writeFile(open(fileName), dir)
    
    def writeFile(self, inputFile, inputDirName):
        from JackTokenizer import JackTokenizer
        from CompilationEngine import CompilationEngine
        import os
        outputFileName = os.path.join(inputDirName, "output",
            os.path.splitext(os.path.basename(inputFile.name))[0] + ".xml")
        
        if(not os.path.exists(os.path.dirname(outputFileName))):
            os.makedirs(os.path.dirname(outputFileName))
        outputFile = open(outputFileName, 'w')
        tokenizer = JackTokenizer(inputFile)
        engine = CompilationEngine(tokenizer, outputFile)
        tokenizer.advance()
        engine.compileClass()
    
    def writeTokenizerFile(self, inputFile, inputDirName):
        from JackTokenizer import JackTokenizer
        import os
        outputFileName = os.path.join(inputDirName, "output", 
            os.path.splitext(os.path.basename(inputFile.name))[0] + ".xml")
        if(not os.path.exists(os.path.dirname(outputFileName))):
            os.makedirs(os.path.dirname(outputFileName))
        outputFile = open(outputFileName, 'w')
        outputFile.write("<tokens>\n")
        tokenizer = JackTokenizer(inputFile)
        while(tokenizer.hasMoreTokens()):
            tokenizer.advance()
            if tokenizer.tokenType == JackTokenizer.KEYWORD:
                outputFile.write("\t<keyword>" + tokenizer.currentToken + "</keyword>\n")
            elif tokenizer.tokenType == JackTokenizer.SYMBOL:
                outputFile.write("\t<symbol>")
                if tokenizer.currentToken == "&":
                    outputFile.write("&amp;")
                elif tokenizer.currentToken == "<":
                    outputFile.write("&lt;")
                elif tokenizer.currentToken == ">":
                    outputFile.write("&gt;")
                elif tokenizer.currentToken == "\"":
                    outputFile.write("&quot;")
                else:
                    outputFile.write(tokenizer.currentToken)
                outputFile.write("</symbol>\n")
            elif tokenizer.tokenType == JackTokenizer.IDENTIFIER:
                outputFile.write("\t<identifier>" + tokenizer.currentToken + "</identifier>\n")
            elif tokenizer.tokenType == JackTokenizer.INT_CONST:
                outputFile.write("\t<integerConstant>" + tokenizer.currentToken + "</integerConstant>\n")
            elif tokenizer.tokenType == JackTokenizer.STRING_CONST:
                outputFile.write("\t<stringConstant>" + tokenizer.currentToken + "</stringConstant>\n")
        
        outputFile.write("</tokens>\n")
