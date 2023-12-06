# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import argparse
import os
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

answer = ""

#####

print()
print("RESULT")
if test_mode:
    if answer == test_answer:
        print("✅ ", end='')
    else:
        print("❌ ", end='')
print(answer)