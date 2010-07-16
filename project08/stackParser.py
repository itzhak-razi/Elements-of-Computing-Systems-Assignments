class Parser:

    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8 

    ARITHMETIC_COMMANDS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

    def __init__(self, fileInput):
        import re
        file = fileInput.read()
        lines = file.splitlines()
        self.commands = []
        while len(lines) > 0:
            current = lines.pop(0)
            stripped = current.strip()
            if not(re.match("//", stripped) or len(stripped) == 0):
                self.commands.append(stripped)
        self.counter = -1

    def current(self):
        return self.commands[self.counter]

    def hasMoreCommands(self):
       return self.counter + 1 < len(self.commands) 

    def advance(self):
        self.counter += 1
        return self.commands[self.counter]
    
    def commandType(self):
        import re
        for command in Parser.ARITHMETIC_COMMANDS:
            if command == self.current():
                return Parser.C_ARITHMETIC
        if re.match("push", self.current()):
            return Parser.C_PUSH
        elif re.match("pop", self.current()):
            return Parser.C_POP
        elif re.match("label", self.current()):
            return Parser.C_LABEL
        elif re.match("if-goto", self.current()):
            return Parser.C_IF
        elif re.match("goto", self.current()):
            return Parser.C_GOTO
        elif re.match("function", self.current()):
            return Parser.C_FUNCTION
        elif re.match("call", self.current()):
            return Parser.C_CALL
        elif re.match("return", self.current()):
            return Parser.C_RETURN



    def arg1(self):
        import re
        if self.commandType() == Parser.C_RETURN:
            raise TypeError("Trying to get the first argument on a return command")

        if self.commandType() == Parser.C_ARITHMETIC:
            result=re.match("\w+", self.current())
            return result.group(0)
        else:
            result = re.search("\w+\s+(\w+)", self.current())
            return result.group(1)
             
    def arg2(self):
        import re
        type = self.commandType()
        if type != Parser.C_PUSH and type != Parser.C_POP and type != Parser.C_FUNCTION and type != Parser.C_CALL:
           raise TypeError("Cannot get the second argument for this command")

        result = re.search("\w+\s+\w+\s+(\w+)", self.current())
        return result.group(1)
