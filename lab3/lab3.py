# 8.10.11
# sin(ln(y) + 2) * cos(x)
from math import sin, cos, log

stack = []

PC = 0  # command number
TC = 1  # tact
PS = 0  # sign

STACK_SIZE = 6
EXPONENT_WIDTH = 8
MANTISS_WIDTH = 10

WIDTH = 1 + EXPONENT_WIDTH + MANTISS_WIDTH
EXP_SHIFT = 2 ** (EXPONENT_WIDTH - 1) - 1
MAXIMUM_EXP = 2 ** EXPONENT_WIDTH - 1 - EXP_SHIFT
MINIMUM_EXP = -EXP_SHIFT

# decor
# =====================


def seeStack():
    print('Stack:')
    for i in range(STACK_SIZE):
        if i < len(stack):
            string = seeBin(stack[i]) + " :  " + str(seeNumber(stack[i]))
            print(f'    {i}: {string}')
        else:
            print(f"    {i}: -----------------------")
    print("\n")


def wait():
    input("press Enter")


def draw():
    seeStack()
    print(f"TC = {TC % 2 + 1}")
    print(f"PC = {PC}")
    print(f"PS = {PS}\n")


def firstTact(operation, str=" "):
    global TC, PC
    PC += 1
    TC += 1
    print(f"{operation}: {str}")
    draw()
    wait()


def secondTact(operation, num):
    global TC, PS
    TC += 1
    if float(num) < 0:
        PS = 1
    else:
        PS = 0
    print(f"{operation}: {num}")
    draw()
    wait()


def seeInfo():
    print(f's {"e" * EXPONENT_WIDTH} M.{"m" * MANTISS_WIDTH} decimal value')
    num = [0] + [0] * (EXPONENT_WIDTH - 1) + [1] + [0] * MANTISS_WIDTH
    print(f'{seeBin(num)} {seeNumber(num)} = мінімальне за абсолютною величиною ненульове представлення')
    num = [0] + [1] * (EXPONENT_WIDTH - 1) + [0] + [1] * MANTISS_WIDTH
    print(f'{seeBin(num)} {seeNumber(num)} = максимальне додатнє представлення (2 - 2^(-{MANTISS_WIDTH})) * 2^{MAXIMUM_EXP - 1}')
    num = [1] + [1] * (EXPONENT_WIDTH - 1) + [0] + [1] * MANTISS_WIDTH
    print(f'{seeBin(num)} {seeNumber(num)} = мінімальне від’ємне преставлення')
    num = numToBin(1.0)
    print(f'{seeBin(num)} {seeNumber(num)} = число +1,0Е0')
    num = [0] + [1] * EXPONENT_WIDTH + [0] * MANTISS_WIDTH
    print(f'{seeBin(num)} {seeNumber(num)} = значення +inf')  # +∞
    num = [1] + [1] * EXPONENT_WIDTH + [0] * MANTISS_WIDTH
    print(f'{seeBin(num)} {seeNumber(num)} = значення -inf')  # -∞
    num = [0] + [0] * (EXPONENT_WIDTH) + [0] * (MANTISS_WIDTH - 1) + [1]
    print(f'{seeBin(num)} {seeNumber(num)} = будь-який варіант для ненормалізованого ЧПТ')
    num = [0] + [0] * (EXPONENT_WIDTH + MANTISS_WIDTH)
    print(f'{seeBin(num)} {seeNumber(num)} = +0.0')
    num = [1] + [0] * (EXPONENT_WIDTH + MANTISS_WIDTH)
    print(f'{seeBin(num)} {seeNumber(num)} = -0.0')
    num = [0] + [1] * (EXPONENT_WIDTH) + [0] * (MANTISS_WIDTH - 1) + [1]
    print(f'{seeBin(num)} {seeNumber(num)} = будь-який варіант для NaN-значення')


#  IEEE 754
# =======================
def setExp(arr, exp):
    exp += EXP_SHIFT
    pos = EXPONENT_WIDTH
    while exp:
        arr[pos] = exp % 2
        pos -= 1
        exp = exp // 2


def isZero(bin):
    _, exp, mant = binCut(bin)

    if mant != 0:
        return False

    if exp != MINIMUM_EXP:
        return False

    return True


def isInfinity(bin):
    _, exp, mant = binCut(bin)

    if mant != 0:
        return False

    if exp != MAXIMUM_EXP:
        return False

    return True


def isNan(bin):
    if isInfinity(bin):
        return False

    exp = binCut(bin)[1]
    return exp == MAXIMUM_EXP


def isDenormalized(bin):
    if isZero(bin):
        return False

    exp = binCut(bin)[1]
    return exp == MINIMUM_EXP

# bin array cutter


def binCut(bin):
    sign = bin[0]

    exponent = 0
    for i in range(1, EXPONENT_WIDTH + 1):
        exponent *= 2
        exponent += bin[i]

    exponent -= EXP_SHIFT

    mantiss = 0
    for i in range(EXPONENT_WIDTH + 1, WIDTH):
        mantiss *= 2
        mantiss += bin[i]

    return sign, exponent, mantiss

# bin array to float


def seeNumber(bin):
    sign, exp, mant = binCut(bin)

    if isZero(bin):
        if sign == 1:
            return ('-0.0')
        else:
            return ('+0.0')
    elif isInfinity(bin):
        if sign == 1:
            return ('-inf')
        else:
            return ('+inf')
    elif isNan(bin):
        return ('NaN')
    elif isDenormalized(bin):
        return ((-1) ** sign) * (2 ** exp) * (mant / (2 ** MANTISS_WIDTH))
    else:
        return ((-1) ** sign) * (2 ** exp) * (1 + mant / (2 ** MANTISS_WIDTH))

# bin array to string


def seeBin(bin):
    arr = []

    # sign
    arr.append(str(bin[0]))
    # exponenta
    arr.append(''.join(map(str, bin[1:EXPONENT_WIDTH + 1])))
    # mantissa
    arr.append(''.join(map(str, bin[EXPONENT_WIDTH + 1:])))

    mantiss_forgotten_bit = ''

    if isZero(bin):
        mantiss_forgotten_bit = '0'
    elif isInfinity(bin):
        mantiss_forgotten_bit = '1'
    elif isNan(bin):
        mantiss_forgotten_bit = '0'
    else:
        if isDenormalized(bin):
            mantiss_forgotten_bit = '0'
        else:
            mantiss_forgotten_bit = '1'
    arr.insert(2, mantiss_forgotten_bit)

    return ' '.join(arr)

# int to bin array


def numToBin(num):
    bin = [0] * WIDTH

    string = str(num)
    # sign
    sign = 0
    if string.startswith("-"):
        sign = 1
        string = string[1:]
    elif string.startswith("+"):
        string = string[1:]

    # float split
    if '.' in string:
        a1, a2 = string.split('.')
    else:
        a1, a2 = string, '0'
    div = 10 ** len(a2)
    a1, a2 = int(a1), int(a2)

    # integer part of number
    binA1 = []
    while a1:
        binA1.insert(0, a1 % 2)
        a1 = a1 // 2

    # +/- inf
    if len(binA1) > MAXIMUM_EXP:  # +/- inf
        bin[0] = sign
        setExp(bin, MAXIMUM_EXP)

    else:
        # fractional part of a number
        binA2 = []
        while a2 and len(binA2) < EXP_SHIFT + MANTISS_WIDTH + 1:
            a2 *= 2
            binA2.append(a2 // div)
            a2 %= div

        # integer number
        if binA1:
            bin[0] = sign
            exponent = len(binA1) - 1
            setExp(bin, exponent)
            temp = binA1[1:] + binA2
            for i in range(min(len(temp), MANTISS_WIDTH)):
                bin[1 + EXPONENT_WIDTH + i] = temp[i]
        # float number
        else:
            exponent = -1
            for i in range(len(binA2)):
                if binA2[i] == 1:
                    exponent = i + 1
                    break
            # +/- 0.0
            if exponent == -1 or exponent > EXP_SHIFT + MANTISS_WIDTH:
                bin[0] = sign
            # denormalized
            elif exponent > EXP_SHIFT:
                bin[0] = sign
                for i in range(min(len(binA2) - EXP_SHIFT, MANTISS_WIDTH)):
                    bin[1 + EXPONENT_WIDTH + i] = binA2[EXP_SHIFT + i]
            # |number| < 1
            else:
                bin[0] = sign
                setExp(bin, -exponent)
                for i in range(min(len(binA2) - exponent, MANTISS_WIDTH)):
                    bin[1 + EXPONENT_WIDTH + i] = binA2[exponent + i]

    return bin

# operations
# ===================


def push(num, b=True):
    if (len(stack) > STACK_SIZE):
        raise ValueError("Stack overflow")
    if b:
        firstTact("Push", str(num))
        binNum = numToBin(num)
        stack.append(binNum)
        secondTact("Push", num)
    else:
        binNum = numToBin(num)
        stack.append(binNum)


def pop(operation=" ", b=True):
    if (len(stack) < 1):
        raise ValueError(f"\nDurring: {operation}\nError: Stack empty")
    if b:
        firstTact("Pop", str(num))
        num = stack.pop()
        secondTact("Pop", seeNumber(num))
        return num
    else:
        return stack.pop()


def ln():
    firstTact("Ln")
    bin = pop("Ln", False)
    num = seeNumber(bin)
    push(log(num), False)
    secondTact("Ln", num)


def reverse():
    firstTact("Reverse")
    a = seeNumber(pop("Reverse", False))
    b = seeNumber(pop("Reverse", False))
    push(a, False)
    push(b, False)
    secondTact("Reverse", b)


def plus():
    firstTact("Plus")
    a = seeNumber(pop("Plus", False))
    b = seeNumber(pop("Plus", False))
    push(a+b, False)
    secondTact("Plus", b)


def sinn():
    firstTact("Sin")
    a = seeNumber(pop("Sin", False))
    push(sin(a), False)
    secondTact("Sin", a)


def coss():
    firstTact("Cos")
    a = seeNumber(pop("Cos", False))
    push(cos(a), False)
    secondTact("Cos", a)


def mult():
    firstTact("Mult")
    a = seeNumber(pop("Mult", False))
    b = seeNumber(pop("Mult", False))
    push(a*b, False)
    secondTact("Mult", b)


def main(x=5, y=3):

    print("\nVariant: 8.10.11 \n")
    print("Do you want to see info? y|n")
    b = input("")
    if b == "y" or b == "Y":
        seeInfo()

    # 8.10.11
    # sin(ln(y) + 2) * cos(x)
    print("\nPlease enter the variables for sin(ln(y) + 2)*cos(x)")

    x = input("\nx: ")
    y = input("y: ")

    print("\n")

    #         Formula iteration             Stack:
    push(x)   # x                           { x }
    push(2)   # 2                           { 2, x }
    push(y)   # y                           { y, 2, x }
    ln()      # ln(y)                       { ln(y), 2, x }
    plus()    # ln(y) + 2                   { ln(y) + 2, x }
    sinn()    # sin(ln(y) + 2)              { sin(ln(y) + 2), x }
    reverse()  # x                           { x, sin(ln(y) + 2) }
    coss()    # cos(x)                      { cos(x), sin(ln(y) + 2) }
    mult()    # sin(ln(y) + 2) * cos(x)     { sin(ln(y) + 2) * cos(x) }

    ans = seeNumber(pop("Answer", False))
    print(f"\nAnswer = {ans}\n")
    return ans


main()
