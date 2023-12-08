# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

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

def get_result(input: str, part_b: bool = False):
    return ""

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

