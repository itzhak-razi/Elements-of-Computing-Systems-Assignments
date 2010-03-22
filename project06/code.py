def dest(value):
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
    result = ""
    if "M" in value:
        result += "1"
    elif "A" in value:
        result += "0"

    return result
