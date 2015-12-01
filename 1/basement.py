#!/usr/bin/python

import sys

floor = 0;

if len(sys.argv) > 1:
    paren = sys.argv[1]
    for i in range(0, len(paren)):
        if paren[i] == '(':
            floor += 1
        if paren[i] == ')':
            floor -= 1
        if floor == -1:
            print i+1
            break

