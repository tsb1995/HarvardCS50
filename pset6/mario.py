from cs50 import get_int

def get_int_in_range():
    while True:
        n = get_int("Height:")
        if n in range(1,9):
            break
    return n
height = get_int_in_range()
for k in range(height):
    print(" "*(height-k-1), end="")
    print("#"*(k+1), end="")
    print("  ", end="")
    print("#"*(k+1))