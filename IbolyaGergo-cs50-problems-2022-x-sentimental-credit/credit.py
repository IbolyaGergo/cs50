# TODO
from cs50 import get_string

# Making sure the input is numeric
while True:
    number = get_string("Number: ")
    if number.isnumeric():
        break

# Luhn's Algorithm to check if the credit card number is valid


def checksum(number):

    revnumber = number[::-1]
    mult = ""
    for digit in revnumber[1::2]:
        mult += str(2 * int(digit))

    not_mult = revnumber[::2]

    sum = 0
    for digit in (mult + not_mult):
        sum += int(digit)
    print(sum)
    if str(sum)[-1] == "0":
        return True
    else:
        return False


if checksum(number):
    if len(number) == 15 and int(number[0]) == 3 and int(number[1]) in (4, 7):
        card = "AMEX"
    elif len(number) == 16 and int(number[0]) == 5 and int(number[1]) in range(1, 6):
        card = "MASTERCARD"
    elif (len(number) == 13 or len(number) == 16) and int(number[0]) == 4:
        card = "VISA"
    else:
        card = "INVALID"
else:
    card = "INVALID"
print(card)