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


seeds = re.search("^seeds: (.*)\n", input).groups()[0].split()
seeds = list(map(lambda seed: int(seed), seeds))

maps = {
  "seed_to_soil": get_map("seed", "soil"),
  "soil_to_fertilizer": get_map("soil", "fertilizer"),
  "fertilizer_to_water": get_map("fertilizer", "water"),
  "water_to_light": get_map("water", "light"),
  "light_to_temperature": get_map("light", "temperature"),
  "temperature_to_humidity": get_map("temperature", "humidity"),
  "humidity_to_location": get_map("humidity", "location"),
}

print("Entries in")
for key, map in maps.items():
    print(f"{key}: {len(map)}")

print("Seeds: ", end="")
for seed in seeds:
    print(seed, end=" ")
print()

print("---")

answer = math.inf

for seed in seeds:
    print(f"Processing {seed}")

    conversion = seed

    for map_name, map in maps.items():
        new_conversion = conversion
        for entry in map:
          seed_in_entry = conversion >= entry[1] and conversion < entry[1] + entry[2]
          if seed_in_entry:
            new_conversion = conversion - (entry[1] - entry[0])
            print(f"{conversion} -{map_name}:{entry}-> {new_conversion}")
        if conversion == new_conversion:
            print(f"No change in {map_name}")
        conversion = new_conversion

    if conversion < answer:
        answer = conversion


#####

print()
print("RESULT")
if test_mode:
    if answer == test_answer:
        print("✅ ", end='')
    else:
        print("❌ ", end='')
print(answer)