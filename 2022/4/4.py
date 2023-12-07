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

def range_within_range(a: range, b: range):
  return a.start <= b.start and a.stop >= b.stop

def range_overlaps_range(a: range, b: range):
  print(f"{a.start} {b.start}")
  print(f"{a.stop} {b.stop}")
  return (a.start >= b.start and a.start <= b.stop) or (a.stop >= b.start and a.stop <= b.stop)

def get_result(input: str, part_b: bool = False):
    
    section_assignments = input.split('\n')

    fully_overlapped_assignments = 0
    partially_overlapped_assignments = 0

    for section_assignment in section_assignments:
      elf_assignments = list(map(lambda x: (
        range(int(x.split('-')[0]), int(x.split('-')[1]))
      ), section_assignment.split(',')))

      print(f"{elf_assignments[0]} {elf_assignments[1]}", end='')
      
      if range_within_range(elf_assignments[0], elf_assignments[1]) or range_within_range(elf_assignments[1], elf_assignments[0]):
        print("!")
        fully_overlapped_assignments += 1

      if range_overlaps_range(elf_assignments[0], elf_assignments[1]) or range_overlaps_range(elf_assignments[1], elf_assignments[0]):
        print("@")
        partially_overlapped_assignments += 1

    if not part_b:
      return fully_overlapped_assignments
    else:
      return partially_overlapped_assignments

#####

def check_result(result: str, answer: str):
  if test_answer_a == "":
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
       aocd.submit(int(result), part="b", day=int(day), year=int(year))

if test_a_success:
  if inquirer.confirm("Test succeeded on one part a, run on real data?"):
    print("RUNNING PART A")
    result = get_result(input)

    print("RESULT PART A: ", end="")
    print(result)

    if inquirer.confirm(f"Submit result ({result})?"):
       [year, day] = os.path.dirname(__file__).split(os.path.sep)[-2:]
       aocd.submit(result, part="a", day=int(day), year=int(year))

