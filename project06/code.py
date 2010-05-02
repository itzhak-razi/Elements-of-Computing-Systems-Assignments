def dest(value):
    if(value == None):
        return "000"

    #Do not change order in array
    possible = ["A", "D", "M"]
    result = ""
    for current in possible:
        if current in value:
            result += "1"
        else:
            result += "0" 
    return result


def comp(value):
    import re
    result = ""
    if "M" in value:
        result += "1"
    else:
        result += "0"

    secondVar = "(A|M)"
    plusOneRegex = "\s*\+\s*1"
    minusOneRegex = "\s*-\s*1"
    if "0" == value:
        result += "101010"
    elif "1" == value:
        result += "111111"
    elif "-1" == value:
        result += "111010"
    elif "D" == value:
        result += "001100"
    elif re.match(secondVar, value):
        result += "110000"
    elif "!D" == value:
        result += "001101"
    elif re.match("!" + secondVar, value):
        result += "110001"
    elif "-D" == value:
        result += "001111"
    elif re.match("-" + secondVar, value): 
        result += "110011"
    elif re.match("D" + plusOneRegex, value): #D+1
        result += "011111"
    elif re.match(secondVar + plusOneRegex, value):
        result += "110111"
    elif re.match("D" + minusOneRegex, value):
        result += "001110"
    elif re.match(secondVar + minusOneRegex, value):
        result += "110010"
    elif re.match("D\s*\+\s*" + secondVar, value):
        result += "000010"
    elif re.match("D\s*-\s*" + secondVar, value):
        result += "010011"
    elif re.match(secondVar + "\s*-\s*D", value):
        result += "000111"
    elif re.match("D\s*&\s*" + secondVar, value):
        result += "000000"
    elif re.match("D\s*\|\s*" + secondVar, value):
        result += "010101"
    return result

def jump(value):
    if value == None:
        return "000"
    result = ""
    import re
    possible = ["L|NE|MP", "[^N]E|MP", "G|NE|MP"]
    for current in possible:
        if re.search(current, value):
            result += "1"
        else:
            result += "0"
    return result
