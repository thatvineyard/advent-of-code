# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import argparse
import math
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

cards = input.split('\n')

sum = 0

print("Going through cards")
for card in cards:
    if not card or card == '':
        continue
    print('.', end='')


    [card_id, card_spec] = card.split(':')
    [card_winning_numbers, card_numbers] = card_spec.split('|')

    matches = []

    card_winning_numbers_list = card_winning_numbers.split(' ')
    card_numbers_list = card_numbers.split(' ')

    for card_number in card_numbers_list:
      if not card_number or card_number == '':
          continue
      if card_number in card_winning_numbers.split(' '):
          matches.append(card_number)
    
    if(len(matches) > 0):
      points = math.pow(2, len(matches) - 1)
      sum += points

print()

answer = sum

#####

if test_mode:
    if answer == test_answer:
        print("✅ ", end='')
    else:
        print("❌ ", end='')
print(answer)