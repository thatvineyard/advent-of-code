# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import argparse
import collections
import math
import os
import re

dir = os.path.dirname(__file__)

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("-t", "--test", action="store_true")
args = parser.parse_args()

test_mode = args.test

if test_mode:
    test_input_file = open(file=os.path.join(dir, "./test_input.txt"), mode="r")
    test_answer_file = open(file=os.path.join(dir, "./test_answer.txt"), mode="r")
    input = test_input_file.read()
    test_answer = int(test_answer_file.read())
else:
    input_file = open(file=os.path.join(dir, "input.txt"), mode="r")
    input = input_file.read()

#####

digit_regex="[0-9]"
number_regex="[0-9]+"
symbol_regex="[^0-9\.]"

Coordinate = collections.namedtuple('coord', ['line', 'col'])

lines = input.split()

symbol_coordinates: list[Coordinate] = []

active_cells = []

print("Finding symbols", end="")
for line_index, line in enumerate(lines):
    print(".", end="")
    active_cells.append([False for i in range(len(line))])
    
    digits = re.finditer(symbol_regex, line)
    for digit in digits:
        if digit.end() - digit.start() > 1:
            raise Exception(f'Regex should only have found one character but found "{digit.group()}"')

        symbol_coordinates.append(Coordinate(line_index,digit.start()))

print()

print("Targeting cells around symbols", end="")
for symbol_coordinate in symbol_coordinates:
    print(".", end="")
    min_line_index=max(0, min(symbol_coordinate.line - 1, len(lines)))
    max_line_index=max(0, min(symbol_coordinate.line + 2, len(lines)))

    selected_lines = lines[min_line_index:max_line_index]

    for line_index, line in enumerate(selected_lines):
        min_col_index=max(0, min(symbol_coordinate.col - 1, len(line)))
        max_col_index=max(0, min(symbol_coordinate.col + 2, len(line)))

        selected_cols=line[min_col_index:max_col_index]
        
        digits = re.finditer(digit_regex, selected_cols)
        for digit in digits:
            if digit.end() - digit.start() > 1:
                raise Exception(f'Regex should only have found one number but found "{digit.group()}"')
            digit_coordinate = Coordinate(line_index + min_line_index, digit.start() + min_col_index)
            digit_in_input = lines[digit_coordinate.line][digit_coordinate.col]
            if digit.group() != digit_in_input:
                raise Exception(f'Found number "{digit.group()}" did not match number found in input string ({digit.group()}) at that coordinate ({digit_coordinate})')

            active_cells[digit_coordinate.line][digit_coordinate.col] = True
print()

print("Summing targeted cells: ", end='')
sum = 0
for line_index, line in enumerate(lines):
    
    numbers = re.finditer(number_regex, line)
    for number in numbers:
        active=False
        for number_col_index in range(number.start(), number.end()):
            if active_cells[line_index][number_col_index]:
                active=True
                continue
        if active:
            number = int(number.group())
            print(f'{number}, ', end='')
            sum += number
print()


answer = sum

#####

if test_mode:
    if answer == test_answer:
        print("✅ ", end='')
    else:
        print("❌ ", end='')
print(answer)