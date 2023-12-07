# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import argparse
from functools import cmp_to_key
import os
dir = os.path.dirname(__file__)

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("-t", "--test", action="store_true")
args = parser.parse_args()

test_mode = args.test

if test_mode:
    test_input_file = open(file=os.path.join(dir, "./test_input_0.txt"), mode="r")
    # test_answer_file_a = open(file=os.path.join(dir, "./test_answer_a_0.txt"), mode="r")
    test_answer_file_b = open(file=os.path.join(dir, "./test_answer_b_0.txt"), mode="r")
    input = test_input_file.read()
    # test_answer = int(test_answer_file_a.read())
    test_answer = int(test_answer_file_b.read())
else:
    input_file = open(file=os.path.join(dir, "input.txt"), mode="r")
    input = input_file.read()

#####

def card_value(card_char: str):
    match card_char:
        case 'A':
            return 14
        case 'K':
            return 13
        case 'Q':
            return 12
        # case 'J':
        #     return 11
        case 'T':
            return 10
        case 'J':
            return 0
        case _:
            return int(card_char)

def card_is_joker(card):
   return card_value(card) == 0

def get_sets_from_cards(cards):
    # if "J" in cards:
    #   print(f"{cards}")

    number_of_each_card = {}
    number_of_jokers = 0
    for card in cards:
        if card_is_joker(card):
          number_of_jokers += 1
        else:
          if card not in number_of_each_card:
            number_of_each_card[card] = 0
          number_of_each_card[card] += 1
    # unique_cards = list(set(cards))

    number_of_each_card = dict(sorted(number_of_each_card.items(), key=lambda x: card_value(x[0]), reverse=True))

    if len(number_of_each_card) == 0:
      number_of_each_card['J'] = number_of_jokers
    else:
      highest_card_set = max(number_of_each_card, key=number_of_each_card.get)
      number_of_each_card[highest_card_set] += number_of_jokers

    sets_of_cards = {
        5: [],
        4: [],
        3: [],
        2: [],
        1: [],
    }
    for set_value, set_amount in number_of_each_card.items():
      sets_of_cards[set_amount].append(set_value)
    
    # if "J" in cards:
    #   print(sets_of_cards)


    return sets_of_cards


def compare_highest_cards(hand_a, hand_b):
    for cards in zip(hand_a[0], hand_b[0]):
      if card_value(cards[0]) != card_value(cards[1]):
          return card_value(cards[1]) - card_value(cards[0])
    return 0



def compare_hands(hand_a, hand_b):
    sets_a = hand_a[1]
    sets_b = hand_b[1]

    for set_number in sets_a:
        
        if len(sets_a[set_number]) + len(sets_b[set_number]) != 0:
          equal_amount_of_cards = len(sets_a[set_number]) == len(sets_b[set_number])
          if not equal_amount_of_cards:
            return len(sets_b[set_number]) - len(sets_a[set_number]) 
          
          if set_number == 3: # for three of a kind we wanna check for full house
            if len(sets_a[set_number-1]) + len(sets_b[set_number-1]) != 0:
              equal_amount_of_cards_in_next_set = len(sets_a[set_number-1]) == len(sets_b[set_number-1])
              if not equal_amount_of_cards_in_next_set:
                return len(sets_b[set_number-1]) - len(sets_a[set_number-1]) 

    return compare_highest_cards(hand_a, hand_b)


hand_strings = input.split('\n')

hands = []

for hand_string in hand_strings:
    (cards, bet) = hand_string.split(' ')
    # cards = sorted(cards, key=lambda x: card_value(x), reverse=True)
    sets = get_sets_from_cards(cards)

    converted_hand = ("".join(cards), sets, int(bet))

    hands.append(converted_hand)

if len(hand_strings) != len(hands):
    raise Exception("Mismatch in hands length")
 

sorted_hands = sorted(hands, key=cmp_to_key(lambda x, y: compare_hands(x,y)))

sum = 0

for i, hand in enumerate(sorted_hands):
  rank = len(sorted_hands) - i
  winnings = hand[2] * rank
  if 'J' in hand[0] or 'J' in hand[0]:
    print("⚠️ ", end='') 
  print(f"{rank}: {hand} -> {winnings}") 
  sum += winnings

answer = sum

#####

print()
print("RESULT")
if test_mode:
    if answer == test_answer:
        print("✅ ", end='')
    else:
        print("❌ ", end='')
print(answer)
