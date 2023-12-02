#!/usr/bin/python

import sys

floor = 0;

if len(sys.argv) > 1:
    paren = sys.argv[1]
    for p in paren:
        if p == '(':
            floor += 1
        if p == ')':
            floor -= 1

print floor
