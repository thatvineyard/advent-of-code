# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import argparse
import math
import os
import re
dir = os.path.dirname(__file__)

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("-t", "--test", action="store_true")
args = parser.parse_args()

test_mode = args.test

if test_mode:
    test_input_file = open(file=os.path.join(dir, "./test_input.txt"), mode="r")
    test_answer_file = open(file=os.path.join(dir, "./test_answer.txt"), mode="r")
    input = test_input_file.read()
    test_answer = int(test_answer_file.read())
else:
    input_file = open(file=os.path.join(dir, "input.txt"), mode="r")
    input = input_file.read()

#####

def get_map(from_keyword: str, to_keyword: str):
  map_name = f"{from_keyword}-to-{to_keyword} map"
  match = re.search(map_name + ":[^\\n]*\\n((?:(?:\d+\W?){3})+)", input)
  rows = match.groups()[0].split('\n')[:-1]
  mapping = list(map(lambda row: list(map(lambda number: int(number), row.split())), rows))
  return mapping

def get_seed_pairs(iterable):
    seed_iterator = iter(iterable)
    return list(zip(seed_iterator, seed_iterator))

seeds = re.search("^seeds: (.*)\n", input).groups()[0].split()
seeds = list(map(lambda seed: int(seed), seeds))

seed_pairs = get_seed_pairs(seeds)

maps = {
  "seed_to_soil": get_map("seed", "soil"),
  "soil_to_fertilizer": get_map("soil", "fertilizer"),
  "fertilizer_to_water": get_map("fertilizer", "water"),
  "water_to_light": get_map("water", "light"),
  "light_to_temperature": get_map("light", "temperature"),
  "temperature_to_humidity": get_map("temperature", "humidity"),
  "humidity_to_location": get_map("humidity", "location"),
}

map_legend = 'sfwlthl'

print("Entries in")
for key, map in maps.items():
    print(f"{key}: {len(map)}")

print("Seeds: ", end="")
for seed_pair in seed_pairs:
    print(seed_pair, end=" ")
print()

print("---")

 
def create_new_lookup(lookup_start, entry_difference, entry_length):
  converted_lookup_start = lookup_start - entry_difference
  new_lookup = (converted_lookup_start, entry_length, -entry_difference)
  return new_lookup
    

def get_new_lookup_numbers(lookup_start, lookup_length, entry_length):
  lookup_start = lookup_start + entry_length
  lookup_length = lookup_length - entry_length
  return (lookup_start, lookup_length)

def calc_lookups(start: int, length: int, map: str | list[int]):
    lookups: list[tuple] = []
    
    lookup_start = start
    lookup_length = length
    non_converted_start = None
    non_converted_amount = 0
    while lookup_length > 0:
      found_lookup = False

      for entry in map:
          entry_start = entry[1]
          entry_end = entry[1] + entry[2]
          entry_length = entry[2]
          entry_difference = entry[1] - entry[0]
          lookup_start_in_entry = lookup_start >= entry_start and lookup_start < entry_end
          min_length = min(entry_start + entry_length - lookup_start, lookup_length)

          if lookup_start_in_entry:
              if non_converted_start: # put in non-conversion lookup
                lookups.append(create_new_lookup(non_converted_start, 0, non_converted_amount))
                non_converted_start = None
                non_converted_amount = 0
                 
              lookups.append(create_new_lookup(lookup_start, entry_difference, min_length))
              (lookup_start, lookup_length) = get_new_lookup_numbers(lookup_start, lookup_length, min_length)
              found_lookup = True
              break
      
      if not found_lookup:
        if not non_converted_start:
           non_converted_start = lookup_start
           non_converted_amount = 1
        else:
          non_converted_amount = non_converted_amount + 1
        (lookup_start, lookup_length) = get_new_lookup_numbers(lookup_start, lookup_length, 1)
      
    if non_converted_start: # put in non-conversion lookup
      lookups.append(create_new_lookup(non_converted_start, 0, non_converted_amount))
      non_converted_start = None
      non_converted_amount = 0
    return lookups
   

def convert(start: int, length: int, maps: list[str | list[int]]):
    if len(maps) < 1:
       return start
    map = maps[0]
    


    lookups = calc_lookups(start, length, map)

    minimum = math.inf
    for lookup in lookups:
      print(f"{map_legend[::-1][len(maps) - 1:][::-1]}: ", end='')
      print(format_lookup(lookup))

      child_minimum = convert(lookup[0], lookup[1], maps[1:])

      if child_minimum < minimum:
        print(f"{map_legend[::-1][len(maps) - 1:][::-1]}: ", end='')
        print(child_minimum)
        minimum = child_minimum

    return minimum
        
def format_lookup(lookup):
    return f"{lookup[0]}...{lookup[0] + lookup[1] - 1} ({lookup[2]}) (amt: {lookup[1]})"
   

answer = math.inf

seed_answers = {}
map_answers = {
  "seed_to_soil": {},
  "soil_to_fertilizer": {},
  "fertilizer_to_water": {},
  "water_to_light": {},
  "light_to_temperature": {},
  "temperature_to_humidity": {},
  "humidity_to_location": {},
}


for seed_pair in seed_pairs:
    print(f"[{seed_pair}]")

    lookup_start = seed_pair[0]
    lookup_end = seed_pair[0] + seed_pair[1]
    lookup_length = seed_pair[1]
    
    result = convert(lookup_start, lookup_length, list(maps.values()))
    if result < answer:
      answer = result


#####

print()
print("RESULT")
if test_mode:
    if answer == test_answer:
        print("✅ ", end='')
    else:
        print("❌ ", end='')
print(answer)