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

class Directory:
  def __init__(self, name: str, parent):  # noqa: F821
    self.name = name
    self.parent = parent
    self.size = 0
    self.combined_size = 0
    self.children: list[Directory] = []

  def add_file(self, size: int):
    self.size += size
  
  def add_child(self, directory):  # noqa: F821
    self.children.append(directory)

def count_dir_size(directory: Directory):
  total_size = directory.size

  total_sum_directory_size = 0

  children_size = 0
  for child in directory.children:
    [children_size, sum_directory_size] = count_dir_size(child)
    total_sum_directory_size += sum_directory_size
  
  total_size += children_size

  if total_size <= 100000:
    print(f"{directory.name}: adding {total_size}")
    total_sum_directory_size += total_size

  return [total_size,  total_sum_directory_size]

def get_result(input: str, part_b: bool = False):
    
    commands = input.split("$")

    root_directory = Directory("root", None)
    current_directory = root_directory

    for command in commands:
      if command == "":
        continue

      cli_command = command.split("\n")[0]
      results = command.split("\n")[1:]

      match cli_command[:3].strip():
        case "cd":
          dir = cli_command[3:].strip()
          if dir == "..":
            current_directory = current_directory.parent
          else:
            print(f"Creating dir {dir}")
            new_directory = Directory(dir, current_directory)
            current_directory.add_child(new_directory)
            current_directory = new_directory
        case "ls":
          for result in results:
            if result == "":
              continue
            if result.split(' ')[0] != "dir":
              current_directory.add_file(int(result.split(' ')[0]))
        case _:
          raise Exception(f"Unknown command {cli_command[:3].strip()}")

    [children_size, size_sum] = count_dir_size(root_directory)

    print(size_sum)

    return size_sum
    

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

