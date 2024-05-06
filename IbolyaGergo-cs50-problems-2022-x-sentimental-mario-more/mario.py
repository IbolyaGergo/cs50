# TODO
from cs50 import get_int

# Prompt the user for the pyramid's height between 1 and 8, inclusive
while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break
# Creating the pyramid
for i in range(n):
    print(" " * (n - i - 1), end="#" * (i + 1))
    print(" " * 2, end="#" * (i + 1))
    print()