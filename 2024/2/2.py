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
    
    reports = input.split("\n")

    unsafe_indeces = []

    for report_index in range(len(reports)):
      report = reports[report_index]
      levels = report.split(" ")

      if not is_report_safe(levels):
        unsafe_indeces.append(report_index)


    if not part_b:
      result = len(reports) - len(unsafe_indeces)
      return result

    if part_b:

      safe_when_dampened_indeces = [] 
      for unsafe_report_index in unsafe_indeces:
        report = reports[unsafe_report_index]

        levels = report.split(" ")
        for remove_index in range(len(levels)):
          dampened_levels = levels.copy()
          dampened_levels.pop(remove_index)
          if is_report_safe(dampened_levels):
            safe_when_dampened_indeces.append(unsafe_report_index)
            break
      
      for safe_when_dampened_index in safe_when_dampened_indeces:
        unsafe_indeces.remove(safe_when_dampened_index)

      result = len(reports) - len(unsafe_indeces)
      return result
            

def is_report_safe(levels):

    prev_level = None
    prev_difference = None

    for level in levels:
      level = int(level)
        
      if prev_level is None:
        prev_level = level
        continue

      difference = level - prev_level

      prev_level = level

      if abs(difference) < 1 or abs(difference) > 3:
          # print(f"difference between {prev_level} and {level} was {difference}")
        return False

      if prev_difference is None:
        prev_difference = difference
        continue

      if prev_difference < 0 and difference > 0:
        return False

      if prev_difference > 0 and difference < 0:
        return False
    
    return True





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

