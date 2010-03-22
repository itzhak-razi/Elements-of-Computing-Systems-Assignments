class Parser:
    
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    JMP_CMDS = ["JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]

    def __init__(self, fileInput):
        file = fileInput.read()
        self.commands = file.splitlines()
        self.counter = 0

    def current(self):
        return self.commands[self.counter].strip()

    def hasMoreCommands(self):
       return self.counter < len(self.commands) 

    def advance(self):
        self.counter += 1 
        return self.commands[self.counter]

    def commandType(self):
        current = self.commands[self.counter].strip()
        if current[0] == '(' and current[len(current)] == ')':
            return Parser.L_COMMAND
        elif current[0] == '@':
            return Parser.A_COMMAND
        else:
            return Parser.C_COMMAND
           
    def symbol(self):
        current = self.commands[self.counter].strip()
        if self.commandType() == Parser.A_COMMAND:
            return current[1:]
        elif self.commandType() == Parser.L_COMMAND:
            return current[1:len(current) - 2] 
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
        current = self.current()
        index = current.find(';')
        if index > -1:
            current = current[:index]
        index = current.find('=')
        if index > -1:
            current = current[index + 1:]
        return current.strip()
         
    def jump(self):
        current = self.current()
        for jmp in Parser.JMP_CMDS:
            if jmp in current:
               return jmp
