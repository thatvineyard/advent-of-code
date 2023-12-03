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
symbol_regex="[*]"

Coordinate = collections.namedtuple('coord', ['line', 'col'])

lines = input.split()

symbol_coordinates: list[Coordinate] = []

active_cells = []

print("Finding symbols", end="")
for line_index, line in enumerate(lines):
    print(".", end="")
    active_cells.append([False for i in range(len(line))])
    
    numbers = re.finditer(symbol_regex, line)
    for number in numbers:
        if number.end() - number.start() > 1:
            raise Exception(f'Regex should only have found one character but found "{number.group()}"')

        symbol_coordinates.append(Coordinate(line_index,number.start()))

print()

print("Targeting cells around symbols", end="")
sum = 0
for symbol_coordinate in symbol_coordinates:
    print(".", end="")
    min_line_index=max(0, min(symbol_coordinate.line - 1, len(lines)))
    max_line_index=max(0, min(symbol_coordinate.line + 2, len(lines)))

    selected_lines = lines[min_line_index:max_line_index]

    found_number_start_coords: list[Coordinate] = []
    number_of_numbers_found = 0

    for line_index, line in enumerate(selected_lines):
        min_col_index=max(0, min(symbol_coordinate.col - 1, len(line)))
        max_col_index=max(0, min(symbol_coordinate.col + 2, len(line)))

        selected_cols=line[min_col_index:max_col_index]
        
        numbers = re.finditer(number_regex, selected_cols)
        for number in numbers:
            number_of_numbers_found += 1
            digit_coordinate = Coordinate(line_index + min_line_index, number.start() + min_col_index)
            digit_in_input = lines[digit_coordinate.line][digit_coordinate.col]

            found_number_start_coords.append(digit_coordinate)
    
    if len(found_number_start_coords) == 2:

        product=1

        for found_number_start_coord in found_number_start_coords:
            line_starting_at_number = lines[found_number_start_coord.line]
            numbers = list(re.finditer(f'{number_regex}', line_starting_at_number))
            if len(numbers) == 0:
                raise Exception(f'Could not find number at beginning of string ({line_starting_at_number})')
            for number in numbers:
                if number.start() <= found_number_start_coord.col and number.end() >= found_number_start_coord.col:
                    product *= int(number.group())

        sum += product
print()


answer = sum

#####

print("\nRESULT: ")
if test_mode:
    if answer == test_answer:
        print("✅ ", end='')
    else:
        print("❌ ", end='')
print(answer)