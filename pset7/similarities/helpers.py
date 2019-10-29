from nltk.tokenize import sent_tokenize
import re
from textwrap import wrap

def lines(a, b):
    """Return lines in both a and b"""
    #USE SETS
    A = set(a.splitlines())
    B = set(b.splitlines())
    return list(A & B)


def sentences(a, b):
    """Return sentences in both a and b"""
    A = set(sent_tokenize(a))
    B = set(sent_tokenize(b))
    return list(A & B)

def getSubstrings(a, n):
    """Returns a set of substrings of size n"""
    output = set()
    temp = len(a) - n + 1
    for i in range(temp):
        output.add(a[i:n + i])
    return output

def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    #Split into lines without /n
    A = a.splitlines()
    B = b.splitlines()
    setA = getSubstrings(a, n)
    setB = getSubstrings(b, n)
    return list(setA & setB)