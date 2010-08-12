class JackAnalyzer:

    def __init__(self, input):
    import os
    import JackTokenizer 
    from JackTokenizer import JackTokenizer
    

    files = []
    ext = os.path.splitext(input)[1]
    if ext == '':
        for currentFile in os.listdir(input):
            file = open(currentFile)


    def writeFile(outputFile):
        outputFile.write("<tokens>\n")
        tokenizer = JackTokenizer(inputFile)
        while(tokenizer.hasMoreTokens()):
            tokenizer.advance()
            if tokenizer.tokenType == JackTokenizer.KEYWORD:
                outputFile.write("<keyword>" + tokenizer.currentToken + "</keyword>\n")
            elif tokenizer.tokenType == JackTokenizer.SYMBOL:
                outputFile.write("<symbol>")
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
                outputFile.write("<identifier>" + tokenizer.currentToken + "</identifier>\n")
            elif tokenizer.tokenType == JackTokenizer.INT_CONST:
                outputFile.write("<integerConstant>" + tokenizer.currentToken + "</integerConstant>\n")
            elif tokenizer.tokenType == JackTokenizer.STRING_CONST:
                outputFile.write("<stringConstant>" + tokenizer.currentToken + "</stringConstant>\n")
        
        outputFile.write("</tokens>\n")
