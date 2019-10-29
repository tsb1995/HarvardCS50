from cs50 import get_string
from sys import argv


def main():

    if len(argv) != 2:
        print("Usage: python bleep.py txt")
        exit(1)

    with open(f"./{argv[1]}", "r") as infile:
        dict = infile.readlines()
        for i in range(0, len(dict)):
            dict[i] = dict[i].rstrip("\n")

    input = get_string("What message would you like to censor?\n")
    new_input = input.split()

    for word in new_input:
        if word.isupper():
            word = word.lower()
            if word in dict:
                length = len(word)
                stars = "*"*length
                word = stars
            word = word.upper()
        else:
            if word in dict:
                length = len(word)
                stars = "*"*length
                word = stars
        print(word, end = " ")
    print("")




if __name__ == "__main__":
    main()
