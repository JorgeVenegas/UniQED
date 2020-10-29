from cs50 import get_int


def main():
    while True:
        inpt = get_int("Number: \n")
        if inpt > 0:
            break

    if check_if_valid(inpt):
        check_for_brand_and_print(inpt)
    else:
        print("INVALID")


def check_if_valid(inpt):
    lngth = len(str(inpt))
    return (lngth in [13, 15, 16]) and check_sum(inpt)


def check_sum(inpt):
    p = 0
    summ = int(0)
    while int(inpt) != 0:
        if p % 2 == 0:
            summ += int(inpt % 10)
        else:
            digit = int(2 * (int(inpt) % 10))
            summ += int((digit / 10) + (digit % 10))
        p += 1
        inpt /= 10
    return (int(summ) % 10) == 0


def check_for_brand_and_print(ipt):
    inpt = int(ipt)
    if 34e13 <= inpt < 35e13 or 37e13 <= inpt < 38e13:
        brand = "AMEX"
    elif 51e14 <= inpt < 56e14:
        brand = "MASTERCARD"
    elif 4e12 <= inpt < 5e12 or 4e15 <= inpt < 5e15:
        brand = "VISA"
    else:
        brand = "INVALID"
    print(brand)


main()