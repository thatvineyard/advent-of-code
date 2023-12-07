# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

from functools import reduce
import os
import secrets

import aocd
import dotenv
import inquirer

dotenv.load_dotenv()

dir = os.path.dirname(__file__)

test_input_file = open(file=os.path.join(dir, "./test_input.txt"), mode="r")
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

def char_priority(char: str):
  prio = ord(char) - ord('a') + 1
  if prio < 0:
    prio += 58
  return prio

def get_result(input: str, part_b: bool = False):
    
    rucksacks = input.split('\n')


    # print(f"{char_priority('a')} {char_priority('z')}")
    # print(f"{char_priority('A')} {char_priority('Z')}")
    total_score = 0

    while len(rucksacks) > 0:
      rucksack_set = rucksacks[:3]
      rucksacks = rucksacks[3:]

      possible_ids = []

      for rucksack in rucksack_set:
        if not part_b:
          first_half = rucksack[:len(rucksack)//2]
          second_half = rucksack[len(rucksack)//2:]

          if rucksack != f"{first_half}{second_half}":
            raise Exception("Split rucksack not correct")

          duplicates = []

          for char in first_half:
            if char in second_half:
                duplicates.append(char)
          
          duplicates = list(set(duplicates))
          scores = list(map(char_priority, duplicates))
          print(scores)
          total_score += reduce(lambda acc, char: char + acc, scores)
        else:
          
          if possible_ids == []:
            new_possible_ids = list(set(rucksack))
          else:
            new_possible_ids = []
            for char in possible_ids:
              if char in rucksack:
                  new_possible_ids.append(char)
          
          possible_ids = new_possible_ids 

      if part_b:   
        total_score += char_priority(possible_ids[0])

    return total_score

#####

print("RUNNING TEST (PART A)")
test_result_a = get_result(test_input)
print("RUNNING TEST (PART B)")
test_result_b = get_result(test_input, True)

print("TEST RESULTS")
print("Part A ", end='')
if test_answer_a == 0:
    print("⏹ ", end="")
else:
  if test_result_a == test_answer_a:
      print("🟩", end="")
  if test_result_a != test_answer_a:
      print(f"🟥 (should be {test_answer_a})", end="")
print(": ", end="")
print(test_result_a)

print("Part B ", end='')
if test_answer_b == 0:
    print("⏹ ", end="")
else: 
  if test_result_b == test_answer_b:
      print("🟩", end="")
  if test_result_b != test_answer_b:
      print(f"🟥 (should be {test_answer_b})", end="")
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

