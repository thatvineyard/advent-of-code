# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import os
import sys

import inquirer
dir = os.path.dirname(__file__)

test_input_file = open(file=os.path.join(dir, "./test_input.txt"), mode="r")
test_answer_a_file = open(file=os.path.join(dir, "./test_answer_a.txt"), mode="r")
test_answer_b_file = open(file=os.path.join(dir, "./test_answer_b.txt"), mode="r")
test_input = test_input_file.read()
test_answer_a = int(test_answer_a_file.read())
test_answer_b = int(test_answer_b_file.read())
input_file = open(file=os.path.join(dir, "input.txt"), mode="r")
input = input_file.read()

#####

def get_result(input: str, part_b: bool = False):
    return ""

#####

print("RUNNING TEST")
test_result_a = get_result(test_input)
test_result_b = get_result(test_input, True)

print("TEST RESULTS")
print("Part A ", end='')
if test_answer_a == "":
    print("⏹", end="")
if test_result_a == test_answer_a:
    print("🟩", end="")
if test_result_a != test_answer_a:
    print("🟥", end="")
print(": ", end="")
print(test_result_a)

print("Part B ", end='')
if test_answer_b == "":
    print("⏹", end="")
if test_result_b == test_answer_b:
    print("🟩", end="")
if test_result_b != test_answer_b:
    print("🟥", end="")
print(": ", end="")
print(test_result_b)

if test_result_b == test_answer_b:
  if inquirer.confirm("Test succeeded on one part b, run on real data?"):
    print("RUNNING PART B")
    result = get_result(input, True)

    print("RESULT PART B: ", end="")
    print(result)

    sys.exit()

if test_result_a == test_answer_a:
  if inquirer.confirm("Test succeeded on one part a, run on real data?"):
    print("RUNNING PART A")
    result = get_result(input)

    print("RESULT PART A: ", end="")
    print(result)

    sys.exit()
