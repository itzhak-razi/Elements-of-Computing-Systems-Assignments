class SymbolTable:
    STATIC = 0
    FIELD = 1
    ARG = 2
    VAR = 3

    def __init__(self):
        self.classTable = dict()
        self.subTable = dict()

    def startSubroutine(self):
        self.subTable = dict()
   
    def define(self, name, identifierType, identifierkind):
        if(kind == SymbolTable.STATIC || kind == SymbolTable.FIELD):
            self.classTable[name] = dict(kind=identifierKind, type=identifierKind)
        else:
            self.subTable[name] = dict(kind=identifierKind, type=identifierKind)
            
    def varCount(self, kind):
        total = 0
        if(kind == SymbolTable.STATIC || kind == SymbolTable.FIELD):
            for key in self.classTable.keys():
                if self.classTable[key]["kind"] == kind:
                    total += 1
        else:
            for key in self.subTable.keys():
                if self.classTable[key]["kind"] == kind:
                    total += 1
        return total

    def kindOf(self, name):
        return self.fieldOf(name, "kind")

    def typeOf(self, name):
        return self.fieldOf(name, "type")

    def indexOf(self, name):
        return self.fieldOf(name, "index")
    
    #Helper method for kindOf, typeOf, and indexOf
    def fieldOf(self, name, field):
        if name in self.subTable:
            return self.subTable[name][field]
        elif name in self.classTable:
            return self.classTable[name][field]
        else:
            raise Exception(name + " not found in either hash table")

