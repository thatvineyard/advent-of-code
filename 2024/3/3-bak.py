# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import os
import re
from typing import List

import aocd
import dotenv
import inquirer

dotenv.load_dotenv()

dir = os.path.dirname(__file__)

def try_get_multiple_file_contents(*filenames: list[str]):
  result = []
  for filename in filenames:
    path = os.path.join(dir, filename)
    if os.path.isfile(path):
      file = open(file=path, mode="r")
      content = file.read()
      file.close()
    else:
      content = ""
    result.append(content)
  return result
     
   
[input, test_input, test_answer_a, test_answer_b] = try_get_multiple_file_contents("input.txt", "test_input.txt", "test_answer_a.txt", "test_answer_b.txt")

#####

def get_result(input: str, part_b: bool = False):
    
    if not part_b:
      operations = re.findall("mul\\((\\d\\d?\\d?),(\\d\\d?\\d?)\\)", input)

      product_sum = 0

      for operation in operations:
        val_a = int(operation[0])
        val_b = int(operation[1])

        product = val_a * val_b

        product_sum += product

      return product_sum 
    
    if part_b:
      operations = re.finditer("mul\\((\\d\\d?\\d?),(\\d\\d?\\d?)\\)", input)
      conditionals = re.finditer("(do\\(\\)|don't\\(\\))", input)

      all_keywords : List[re.Match] = [] 
      
      for operation in operations:
        all_keywords.append(operation)
        
      for conditional in conditionals:
        all_keywords.append(conditional)
 
      product_sum = 0

      all_keywords.sort(key=lambda keyword: keyword.span(0)[0])


      active = True

      for keyword in all_keywords:
        
        if keyword.group() == "do()":
          active = True
          continue
        if keyword.group() == "don't()":
          active = False
          continue

        if active:
          val_a = int(keyword.groups()[0])
          val_b = int(keyword.groups()[1])

          product = val_a * val_b

          product_sum += product

      return product_sum

#####

def check_result(result: str, answer: str):
  if answer == "":
    print("⏹ ")
  else:
    if str(result) == answer:
        print(f"🟩 {result}")
        return True
    if str(result) != answer:
        print(f"🟥 {result} (expected {answer})")
  return False

print("-- TEST A --")
test_result_a = get_result(test_input)
test_a_success = check_result(test_result_a, test_answer_a)
print("---")
print("-- TEST B --")
test_result_b = get_result(test_input, True)
test_b_success = check_result(test_result_b, test_answer_b)
print("---")

if test_b_success:
  if inquirer.confirm("Test succeeded on one part b, run on real data?"):
    print("RUNNING PART B")
    result = get_result(input, True)

    print("RESULT PART B: ", end="")
    print(result)

    if inquirer.confirm(f"Submit result ({result})?"):
       [year, day] = os.path.dirname(__file__).split(os.path.sep)[-2:]
       aocd.submit(result, part="b", day=int(day), year=int(year))

if test_a_success:
  if inquirer.confirm("Test succeeded on one part a, run on real data?"):
    print("RUNNING PART A")
    result = get_result(input)

    print("RESULT PART A: ", end="")
    print(result)

    if inquirer.confirm(f"Submit result ({result})?"):
       [year, day] = os.path.dirname(__file__).split(os.path.sep)[-2:]
       aocd.submit(result, part="a", day=int(day), year=int(year))
       if aocd.models.Puzzle(year=int(year), day=int(day)).answer_a is not None:
         print("Success!")

