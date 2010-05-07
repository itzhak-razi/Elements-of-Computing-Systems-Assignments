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
        for command in ARITHMETIC_COMMANDS:
            if command == current()
                return C_ARITHMETIC
        
        if re.match("push", current()):
            return C_PUSH



    def arg1(self):
        import re
        if commandType() == C_RETURN:
            raise TypeError("Trying to get the first argument on a return command")

        if commandType() == C_ARITHMETIC:
            result=re.match("\w+", current())
            return result.group(0)
        else:
            result = re.search("\w+\s+(\w+)", current)
            return result.group(1)
             
    def arg2(self):
        import re
        type = commandType()
        if type != C_PUSH and type != C_POP and type != C_FUNCTION and type != C_CALL:
           raise TypeError("Cannot get the second argument for this command")

        result = re.search("\w+\s+\w+\s+(\w+)")
        return result.group(1)
