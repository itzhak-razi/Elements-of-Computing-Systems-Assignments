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
    else:
        result += "0"

    return result

def jump(value):
    import re
    possible = ["L|NE|MP", "[^N]E|MP", "G|NE|MP"]
    for current in possible:
        if re.search(current, value):
            result += "1"
        else:
            result += "0"
    return result
