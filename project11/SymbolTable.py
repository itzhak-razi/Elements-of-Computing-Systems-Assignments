class SymbolTable:
    NONE = 0
    STATIC = "static"
    FIELD = 2
    ARG = "argument"
    VAR = "local"

    def __init__(self):
        self.classTable = dict()
        self.subTable = dict()

    def startSubroutine(self):
        self.subTable = dict()
   
    def define(self, name, identifierType, identifierKind):
        print("Name is " + str(name) + " type is " + str(identifierType) + " and kind is " + str(identifierKind))
        varIndex = self.varCount(identifierKind)
        if(identifierKind == SymbolTable.STATIC or identifierKind == SymbolTable.FIELD):
            self.classTable[name] = dict(kind=identifierKind, type=identifierType, index=varIndex)
        else:
            self.subTable[name] = dict(kind=identifierKind, type=identifierType, index=varIndex)
            
    def varCount(self, kind):
        total = 0
        if(kind == SymbolTable.STATIC or kind == SymbolTable.FIELD):
            for key in self.classTable.keys():
                if self.classTable[key]["kind"] == kind:
                    total += 1
        else:
            for key in self.subTable.keys():
                if self.subTable[key]["kind"] == kind:
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
    
    def isDefined(self, name):
        return name in self.classTable or name in self.subTable

    def stringKindOf(self, name):
        constKind = self.kindOf(name)
        if constKind == SymbolTable.STATIC:
            return "static"
        elif constKind == SymbolTable.FIELD:
            return "field"
        elif constKind == SymbolTable.ARG:
            return "arg"
        elif constKind == SymbolTable.VAR:
            return "var"
        else:
            return "none"
