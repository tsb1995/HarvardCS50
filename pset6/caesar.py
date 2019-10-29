from sys import argv
from cs50 import get_string

def main():
    argc = len(argv)
    if argc != 2:
        print("Usage: python caesar.py k")
        exit(1)
    key = argv[1]
    intkey = int(key)
    plaintext = get_string("plaintext: ")
    print("ciphertext: ", end = "")
    for c in plaintext:
        temp = c
        if str.isalpha(c):
            if str.isupper(c):
                temp = chr(((ord(c) - ord("A") + intkey) % 26) + ord("A"))
            if str.islower(c):
                temp = chr(((ord(c) - ord("a") + intkey) % 26) + ord("a"))
            print(temp, end = "")
        else:
            print(temp, end = "")
    print("")
    return 0

main()