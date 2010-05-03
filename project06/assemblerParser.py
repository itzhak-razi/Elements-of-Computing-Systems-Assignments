class Parser:
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    JMP_CMDS = ["JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]

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
        current = self.current()
        if current[0] == '(' and None != re.search('\)', current):
            return Parser.L_COMMAND
        elif current[0] == '@':
            return Parser.A_COMMAND
        else:
            return Parser.C_COMMAND
           
    def symbol(self):
        import re
        current = self.current()
        if self.commandType() == Parser.A_COMMAND:
            result = re.search("@.[^\s(//)]*", current)
            return result.group(0)[1:]
        elif self.commandType() == Parser.L_COMMAND:
            result = re.search("\(..*\)", current)
            return result.group(0)[1:len(current) - 1]
        else:
            raise TypeError("Trying to get symbol on a C_COMMAND")

    
    def dest(self):
        current = self.commands[self.counter]
        index = current.find("=")
        if index > -1:
            return current[:index].strip()
        else:
            return None

    def comp(self):
        import re
        current = self.current()
        index = current.find(';')
        if index > -1:
            current = current[:index]
        index = current.find('=')
        if index > -1:
            current = current[index + 1:]
        result = re.search("[^/]*", current)
        return result.group(0).strip()
         
    def jump(self):
        current = self.current()
        for jmp in Parser.JMP_CMDS:
            if jmp in current:
               return jmp
