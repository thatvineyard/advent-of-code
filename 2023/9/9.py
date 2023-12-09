# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

from msilib import sequence
import os

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

def get_differences(numbers: list[int]):
   result = []

   for i in range(len(numbers) - 1):
      result.append(numbers[i+1] - numbers[i])

   if len(result) != len(numbers) - 1:
      raise Exception(f"Result should be one shorter than input (expected {len(numbers)}, got {len(result)})")
   
   return result
      

def numbers_are_all_zero(numbers: list[int]):
   for number in numbers:
      if number != 0:
         return False
      
   return True

def predict_next(numbers: list[int], part_b: bool):
   if numbers_are_all_zero(numbers):
      return 0
   
   difference = predict_next(get_differences(numbers), part_b)
   if not part_b:
    return numbers[-1] + difference
   else:
    return numbers[0] - difference

def get_result(input: str, part_b: bool = False):
    sequences = input.split("\n")

    sum = 0
    for sequence in sequences:
      sum += predict_next(list(map(lambda x: int(x), sequence.split(' '))), part_b)
       
    return sum



       

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

