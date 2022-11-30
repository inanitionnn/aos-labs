import os
import platform


def fullBit(binStr):
    if len(binStr) < 24:
        return "0" * (24-len(binStr)) + binStr
    return binStr


def fullHex(hexStr):
    if len(hexStr) < 6:
        return "0" * (6-len(hexStr)) + hexStr
    return hexStr


def invertBin(binStr):
    binStr = fullBit(binStr)
    return ''.join('1' if x == '0' else '0' for x in binStr)


def suppCode(binStr):
    inv = invertBin(binStr)[::-1]
    overflow = 0
    res = []
    one = "1" + "0" * (len(inv) - 1)

    for obj in zip(inv, one):
        value = int(obj[0]) + int(obj[1]) + overflow
        overflow = value // 2
        res.append(value % 2)
    if overflow == 1:
        res.append(1)
    res = res[::-1]
    return ''.join(map(str, res))


def intToBin(num):
    try:
        if (int(num) <= 0):
            binStr = bin(int(num))[3:]
            return suppCode(binStr)
        binStr = bin(int(num))[2:]
        return fullBit(binStr)
    except:
        raise Exception("Invalid number")


def binToHex(num):
    return hex(int(num, 2))[2:]


def hexToBin(num):
    return fullBit(bin(int(num, 16))[2:])


def load(reg, num):
    global R1, R2, R3, R4
    match reg:
        case "R1":
            R1 = intToBin(num)
        case "R2":
            R2 = intToBin(num)
        case "R3":
            R3 = intToBin(num)
        case "R4":
            R4 = intToBin(num)
        case _:
            raise Exception("Invalid register")


def loadOp(reg, num):
    global R1, R2, R3, R4, OP
    try:
        num = int(num)
        if (num > 3 or num < 0):
            raise Exception("Invalid index of OP")
    except:
        raise Exception("Invalid index of OP")
    match reg:
        case "R1":
            OP[num] = fullHex(binToHex(R1))
        case "R2":
            OP[num] = fullHex(binToHex(R2))
        case "R3":
            OP[num] = fullHex(binToHex(R3))
        case "R4":
            OP[num] = fullHex(binToHex(R4))
        case _:
            raise Exception("Invalid register")


def shift(reg, num, direct):
    global R1, R2, R3, R4, OP
    arr = ["R1", "R2", "R3", "R4"]
    j = 3
    l = 0
    for i in arr:
        match i:
            case "R1":
                OP[j] = fullHex(binToHex(R1))
            case "R2":
                OP[j] = fullHex(binToHex(R2))
            case "R3":
                OP[j] = fullHex(binToHex(R3))
            case "R4":
                OP[j] = fullHex(binToHex(R4))
        if i == reg:
            break
        l += 1
        j -= 1
    bitStr = ""
    for k in OP:
        bitStr += hexToBin(k)
    if direct == "l":
        newStr = bin(int(bitStr, 2) << int(num))[2:]
    elif direct == "r":
        newStr = bin(int(bitStr, 2) >> int(num))[2:]
    for i in range(l):
        match arr[i]:
            case "R1":
                R1 = fullBit(newStr[24 * 0: 24 * (0 + 1)])
            case "R2":
                R2 = fullBit(newStr[24 * 1: 24 * (1 + 1)])
            case "R3":
                R3 = fullBit(newStr[24 * 2: 24 * (2 + 1)])
            case "R4":
                R4 = fullBit(newStr[24 * 3: 24 * (3 + 1)])


def controller(ArrComm):
    match ArrComm[0]:
        case "Load":
            load(ArrComm[1], ArrComm[2])
        case "LoadOp":
            loadOp(ArrComm[1], ArrComm[2])
        case "LShift":
            shift(ArrComm[1], ArrComm[2], "l")
        case "RShift":
            shift(ArrComm[1], ArrComm[2], "r")
        case _:
            raise Exception("Invalid command")


def draw(line, arr):
    print("==================================================")
    print(f"Команда = {line}")
    print(f"R1 = {R1}   Ins = {arr}")
    print(f"R2 = {R2}   PC = {PC}")
    print(f"R3 = {R3}   TC = {TC % 2 + 1}")
    print(f"R4 = {R4}   PS = {PS}")
    print(f"OP = {OP}\n")


def openFile(file):
    global PC, TC, PS
    f = open(f"{file}", "r")
    for line in f:
        arr = line.split(" ")
        TC += 1
        PC += 1
        if int(arr[2]) > 0:
            PS = 0  # "+"
        else:
            PS = 1  # "-"
        draw(line, arr)
        input("Press Enter to continue...")

        controller(arr)
        TC += 1
        draw(line, arr)
        input("Press Enter to continue...")


def main():
    global R1, R2, R3, R4, PC, TC, PS, OP
    R1, R2, R3, R4 = 0, 0, 0, 0  # registers
    PC = 0  # command number
    TC = 1  # tact
    PS = 0  # sign
    OP = ["0"*6, "0"*6, "0"*6, "0"*6]  # 12 bytes RAM

    print("================================================== ")
    print("Please enter the comand file name:")
    if platform.system() == "Linux":
        fileName = os.path.dirname(__file__) + '/' + input() + ".txt"
    else:
        fileName = os.path.dirname(__file__) + '\\' + input() + ".txt"
    openFile(fileName)


main()
