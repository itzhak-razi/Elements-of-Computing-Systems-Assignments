class Parser:
    
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
       
    def __init__(self, fileInput):
        file = fileInput.read()
        self.commands = file.splitlines()
        self.counter = 0

    def hasMorecommands(self):
       return self.counter < len(self.commands) 

    def advance(self):
        value = self.commands[self.counter]
        self.counter += 1 
        return value

    def commandType(self):
        current = self.commands[self.counter].strip()
        if current[0] == '(' and current[len(current)] == ')':
            return L_COMMAND
        elif current[0] == '@':
            return A_COMMAND
        else:
            return C_COMMAND
           
    def symbol(self):
        current = self.commands[self.counter].strip()
        if self.commandType() == A_COMMAND:
            return current[1:]
        elif self.commandType() == L_COMMAND:
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

    def jump(self):
        jumpCmds = ["JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]

