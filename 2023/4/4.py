# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import argparse
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

cards = input.split('\n')

# clean empty lines
cards = [card for card in cards if cards and not cards == '']


card_results = {}

def amount_of_cards_from_card(select_card_id: int):
  if select_card_id in card_results.keys():
     print("!", end='')
     return card_results[select_card_id]
  
  card = cards[select_card_id - 1]

  if not card or card == '':
      raise ValueError("Expected to see a card here.")

  [card_name, card_spec] = card.split(':')
  [card_winning_numbers, card_numbers] = card_spec.split('|')

  print(card_name)
  card_id = list(re.findall('[0-9]+', card_name))[0]
  card_id = int(card_id)

  if card_id != select_card_id:
    raise ValueError(f'Wrong card id (was {card_id}, expected {select_card_id})')

  matches = []

  card_winning_numbers_list = card_winning_numbers.split(' ')
  card_numbers_list = card_numbers.split(' ')

  for card_number in card_numbers_list:
    if not card_number or card_number == '':
        continue
    if card_number in card_winning_numbers.split(' '):
        matches.append(card_number)
  
  if(len(matches) == 0):
    return 1
  
  child_cards = 0
  for extra_card_number in range(card_id + 1, card_id + 1 + len(matches)):
    print(f'{extra_card_number}', end='')
    try:
      child_cards += amount_of_cards_from_card(extra_card_number)
    except ValueError as error:
      print(error)
      # raise

  number_of_cards = 1 + child_cards

  card_results[select_card_id] = number_of_cards
  
  print()
  return number_of_cards
  



sum = 0

print("Going through cards")
for card_index in range(len(cards)):
  try:
    points = amount_of_cards_from_card(card_index + 1)
  except ValueError as error:
    print(error)
    points = 0
    # raise

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