# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import os
from random import choice
import sys

import aocd
import dotenv
import inquirer
dir = os.path.dirname(__file__)

dotenv.load_dotenv()

test_input_file = open(file=os.path.join(dir, "test_input.txt"), mode="r")
test_input = test_input_file.read()
test_input_file.close()

if os.path.isfile(os.path.join(dir, "test_answer_a.txt")):
  test_answer_a_file = open(file=os.path.join(dir, "test_answer_a.txt"), mode="r")
  test_answer_a_content = test_answer_a_file.read()
  test_answer_a_file.close()
else:
   test_answer_a_content = ""
if os.path.isfile(os.path.join(dir, "test_answer_b.txt")):
  test_answer_b_file = open(file=os.path.join(dir, "test_answer_b.txt"), mode="r")
  test_answer_b_content = test_answer_b_file.read()
  test_answer_b_file.close()
else:
   test_answer_b_content = ""

if test_answer_a_content != "":
  test_answer_a = int(test_answer_a_content)
else:
   test_answer_a = 0

if test_answer_b_content != "":
  test_answer_b = int(test_answer_b_content)
else:
   test_answer_b = 0

input_file = open(file=os.path.join(dir, "input.txt"), mode="r")
input = input_file.read()
input_file.close()

#####

def score(character: str):
   match character:
      case "A" | "X":
         return 1
      case "B" | "Y":
         return 2
      case "C" | "Z":
         return 3

def get_result(input: str, part_b: bool = False):
    
    rounds = input.split('\n')

    score_sum = 0

    for round in rounds:
      if round == "":
         break
      
      [elf_move, player_move] = round.split(' ')
      if not part_b:
        choice_score = score(player_move)       
        result_score = 0

        if score(player_move) == score(elf_move):
          result_score = 3
        if score(player_move) - score(elf_move) == 1 or score(elf_move) == 3 and score(player_move) == 1:
          result_score = 6

        result_score += choice_score
      else:
        print(f"> {elf_move} {player_move}")
        result_score = (ord(player_move) - ord('X')) * 3


        elf_number = ord(elf_move) - ord('A') 
        player_number = ord(player_move) - ord('X')
        adjustment = player_number - 1
        correct_move_number = (elf_number + player_number - 1) % 3
        print(f"{result_score} {elf_number} {adjustment} {correct_move_number}")
        print(f"{chr(elf_number + ord('A'))} {chr(correct_move_number + ord('X'))}")

        result_score += correct_move_number + 1
        print(result_score)
      

      # print(f"{elf_move} {player_move}: {result_score}")
      score_sum += result_score

    return score_sum
          

#####

print("RUNNING TEST")
test_result_a = get_result(test_input)
test_result_b = get_result(test_input, True)

print("TEST RESULTS")
print("Part A ", end='')
if test_answer_a == 0:
    print("⏹ ", end="")
else:
  if test_result_a == test_answer_a:
      print("🟩", end="")
  if test_result_a != test_answer_a:
      print("🟥", end="")
print(": ", end="")
print(test_result_a)

print("Part B ", end='')
if test_answer_b == 0:
    print("⏹ ", end="")
else: 
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

    if inquirer.confirm(f"Submit result ({result})?"):
       [year, day] = os.path.dirname(__file__).split(os.path.sep)[-2:]
       aocd.submit(int(result), part="b", day=int(day), year=int(year))

if test_result_a == test_answer_a:
  if inquirer.confirm("Test succeeded on one part a, run on real data?"):
    print("RUNNING PART A")
    result = get_result(input)

    print("RESULT PART A: ", end="")
    print(result)

    if inquirer.confirm(f"Submit result ({result})?"):
       [year, day] = os.path.dirname(__file__).split(os.path.sep)[-2:]
       aocd.submit(result, part="a", day=int(day), year=int(year))

