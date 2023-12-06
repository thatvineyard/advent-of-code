# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import argparse
import math
import os
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

def get_race(race: tuple[int | int]):
    half_of_races = math.ceil((race[0] + 1) / 2)
    first_winnable_hold_time = math.inf
    for i in range(0, half_of_races + 1):
        # print(f"i: {i}, race[0]: {race[0]}, race[1]: {race[1]} -> {i * (race[0] - i)}")
        if i * (race[0] - i) > race[1]:
            first_winnable_hold_time = i
            break

    last_winnable_hold_time = race[0] - first_winnable_hold_time

    number_of_winnable_hold_times = (last_winnable_hold_time + 1) - first_winnable_hold_time

    print(f"{first_winnable_hold_time} - {last_winnable_hold_time} ({number_of_winnable_hold_times})")

    return number_of_winnable_hold_times

#####

(time_string, distance_string, _) = input.split('\n')

times = map(lambda string: int(string), time_string.split()[1:])
distances = map(lambda string: int(string), distance_string.split()[1:])

races = zip(times, distances)

product = 1

for race in races:
    product *= get_race(race)

answer = product

#####

print()
print("RESULT")
if test_mode:
    if answer == test_answer:
        print("✅ ", end='')
    else:
        print("❌ ", end='')
print(answer)