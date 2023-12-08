# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

from logging import getLevelName
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
     
   
[input, test_input, test_input_b, test_answer_a, test_answer_b] = try_get_multiple_file_contents("input.txt", "test_input.txt", "test_input_b.txt", "test_answer_a.txt", "test_answer_b.txt")

#####

class Node: 
   
   def __init__(self, name: str, left: str, right: str):
      self.name = name
      self.left_key = left
      self.right_key = right
      self.left = None
      self.right = None
  
   def getLeft(self, nodes: dict):
    if self.left:
      return self.left
    
    if not self.left_key:
      raise Exception("Missing left key")
    
    if self.left_key not in nodes.keys():
      raise Exception(f"Left key ({self.left_key}) not in nodes dict")
    
    self.left = nodes.get(self.left_key)

    return self.left
  
   def getRight(self, nodes: dict):
    if self.right:
      return self.right
    
    if not self.right_key:
      raise Exception("Missing right key")
    
    if self.right_key not in nodes.keys():
      raise Exception(f"Right key ({self.right_key}) not in nodes dict")
    
    self.right = nodes.get(self.right_key)

    return self.right

   def traverse(self, instruction: str, nodes: dict):
    match instruction:
        case "L":
          return self.getLeft(nodes)
        case "R":
          return self.getRight(nodes)
        case _:
          raise Exception(f"Unknown instruction '{instruction}'")
  
   def __repr__(self):
      return f"{self.name}: [{self.left_key}, {self.right_key}]"

def all_nodes_end_in_z(nodes: list[Node]):
  count = 0
  for node in nodes:
    if node.name[2] != "Z":
      if count > 2:
        print(f"{count} Zs")
      return False
    else: 
      count += 1

  if count > 2:
    print(f"{count} Zs")
  return True

def get_result(input: str, part_b: bool = False):
    
    
    [instructions, network_paths] = input.split("\n\n")

    start = "AAA"
    goal = "ZZZ"

    nodes: dict[str | Node] = {}

    current_nodes = []

    for network_path in network_paths.split('\n'):
       (name, destinations) = network_path.split(' = ')

       destinations = destinations[1:][:-1:].split(', ')
       
      #  print(destinations)

       nodes[name] = Node(name, destinations[0], destinations[1])
       if name[2] == "A":
         current_nodes.append(nodes[name])

    current_instructions = instructions

    if not part_b:
      steps = 0
      current_node: Node = nodes[start]

      while current_node.name != goal:
        steps += 1

        if current_instructions == "":
          current_instructions = instructions

        # print(f"{current_node} - {current_instructions[0]} ({len(current_instructions)})")
        current_instruction = current_instructions[0]
        current_instructions = current_instructions[1:]
        current_node = current_node.traverse(current_instruction, nodes)
      
      return steps
    
    else:
      steps = {}
      print(current_nodes)
      for current_node in current_nodes:
        while current_node.name[3] != goal:
          steps += 1

          if current_instructions == "":
            current_instructions = instructions

          # print(f"{current_node} - {current_instructions[0]} ({len(current_instructions)})")
          current_instruction = current_instructions[0]
          current_instructions = current_instructions[1:]
          current_node = current_node.traverse(current_instruction, nodes)
        
        
      
      return steps

      

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
test_result_b = get_result(test_input_b, True)
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

