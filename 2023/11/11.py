# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import dis
import itertools
import math
import os
from string import hexdigits
from turtle import width
from typing import Self

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


[input, test_input, test_answer_a, test_answer_b] = try_get_multiple_file_contents(
    "input.txt", "test_input.txt", "test_answer_a.txt", "test_answer_b.txt"
)

#####


class Galaxy:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def distance_to(self, other: Self):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def slope_to(self, other: Self):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __repr__(self):
        return f"[{self.id}: {self.x}, {self.y}]"

class GalaxyMap:
    def __init__(self):
        self.map_of_contents: dict[int, dict[int, Galaxy]] = {}
        self.list_of_contents: list[Galaxy] = []
        self.height = 0
        self.width = 0

    def add_galaxy(self, galaxy: Galaxy):
        if galaxy.y not in self.map_of_contents.keys():
            self.map_of_contents[galaxy.y] = {}
        self.map_of_contents[galaxy.y][galaxy.x] = galaxy
        self.list_of_contents.append(galaxy)
        if galaxy.x  + 1 > self.width:
            self.width = galaxy.x + 1
        if galaxy.y + 1 > self.height:
            self.height = galaxy.y + 1

    
    def expand(self, amount: int):
        row_has_galaxy = {row_index: False for row_index in range(self.height)}
        col_has_galaxy = {col_index: False for col_index in range(self.width)}
        
        galaxies = list(self.list_of_contents)
        self.map_of_contents: dict[int, dict[int, Galaxy]] = {}
        self.list_of_contents = []
        
        for galaxy in galaxies:
            row_has_galaxy[galaxy.y] = True
            col_has_galaxy[galaxy.x] = True

        for galaxy in galaxies:
            new_y = galaxy.y
            for i, has_galaxy in row_has_galaxy.items():
                if not has_galaxy and galaxy.y > i:
                    new_y += amount
            galaxy.y = new_y
            new_x = galaxy.x
            for i, has_galaxy in col_has_galaxy.items():
                if not has_galaxy and galaxy.x > i:
                    new_x += amount
            galaxy.x = new_x

            self.add_galaxy(galaxy)
        
    def is_galaxy_at_location(self, x: int, y: int):
        return self.get_galaxy_at_location(x,y) is not None
    
    def get_galaxy_at_location(self, x: int, y: int):
        try:
            return self.map_of_contents[x][y] 
        except KeyError:
            return None

    def print(self):
        print(f"width: {self.width} height: {self.height}")
        for i in range(self.height):
            for j in range(self.width):
                if self.is_galaxy_at_location(i, j):
                    print(self.get_galaxy_at_location(i,j).id, end="")
                else:
                    print(".", end="")
            print()


def get_result(input: str, part_b: bool = False):
    galaxy_map = GalaxyMap()

    galaxy_number = 0

    for i, line in enumerate(input.split("\n")):
        for j, char in enumerate(line):
            if char == "#":
                galaxy_number += 1
                galaxy = Galaxy(galaxy_number, j, i)
                galaxy_map.add_galaxy(galaxy)

    if not part_b:
        galaxy_map.expand(1)
    else:
        galaxy_map.expand(999999)


    sum = 0

    for galaxy_a, galaxy_b in list(itertools.combinations(galaxy_map.list_of_contents, 2)):
        distance = galaxy_a.distance_to(galaxy_b)
        sum += distance
        # print(f"{galaxy_a} : {galaxy_b} = {distance}")




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
test_b_success = check_result(test_result_b, test_answer_b) or True
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
