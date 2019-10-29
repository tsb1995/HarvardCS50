from cs50 import get_float, get_int
from math import pow

def luhn_alg(num, length):
    sum = 0


    for i in range(length-2, -1, -2):
        temp = int(str_num[i])
        temp = temp*2
        str_temp = str(temp)
        sum += int(str_temp[0])
        if temp > 9:
            sum += int(str_temp[1])

    for i in range(length-1, -1, -2):
        sum += int(str_num[i])

    if (sum % 10) == 0:
        return True
    else:
        return False


while True:
    num = get_int("NUMBER:")
    str_num = str(num)
    length = len(str_num)
    check = False
    digit1 = int(str_num[0])
    digit2 = int(str_num[1])
    luhn = luhn_alg(num, length)
    if luhn == False:
        print("INVALID")
        break
    if length == 13:
        if digit1 == 4:
            type = "VISA"
            break
        else:
            print("INVALID")
            break
    elif length == 15:
        if digit1 == 3 and (digit2 == 4 or digit2 == 7):
            type = "AMEX"
            break
        else:
            print("INVALID")
            break
    elif length == 16:
        if digit1 == 5 and digit2 > 0 and digit2 < 6:
            type = "MASTERCARD"
            break
        elif digit1 == 4:
            type = "VISA"
            break
        else:
            print("INVALID")
            break
    else:
        print("INVALID")
        break
print(type)




