from enum import Enum
from turtle import pos
from typing import List, Tuple
from libraries.solution_manager import PuzzleSolution

class Direction(Enum) :
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SW = (1, -1) 
    W = (0, -1)
    NW = (-1, -1)

    def __repr__(self):
        return self.name

class Solution(PuzzleSolution):
    

    def get_answer_a(self, input: str) -> int | float | str:
        search_word = "XMAS"
        self.lines, self.height, self.width = Solution.get_array_and_size(input)


        hits = 0

        x_locations = self.get_char_locations("X")

        for location in x_locations:
            letters_left = search_word[1:]
            check_distance = 1
            possible_directions = self.possible_directions_a(len( search_word), location)

            while len(letters_left) > 0 and len(possible_directions) > 0:
                # print(f"looking for {letters_left} from {location} in the following directions {self.possible_directions(location)} ")

                succesfull_directions = []
                for direction in possible_directions:
                    offset = tuple(x * check_distance for x in direction.value)
                    check_location = tuple(map(sum,zip(location,offset)))
                    
                    letter = self.lines[check_location[0]][check_location[1]]
                    
                    is_letter_correct = letter == letters_left[0]
                    # print(f"{check_location} -> {letter} {is_letter_correct}")

                    if is_letter_correct:
                        succesfull_directions.append(direction)

                possible_directions = succesfull_directions
                check_distance += 1
                letters_left = letters_left[1:]
            
            # print(letters_left)
            if letters_left == "":
                hits += len(possible_directions)

        return hits

    def get_char_locations(self, char):
        x_locations: List[Tuple[int, int]] = []
        for y_coord in range(self.height):
            for x_coord in range(self.width):
                if self.lines[y_coord][x_coord] == char:
                    x_locations.append((y_coord, x_coord))
        return x_locations



    def get_answer_b(self, input: str) -> int | float | str:
        self.lines, self.height, self.width = Solution.get_array_and_size(input)
        search_word = "MAS"
        distance_to_middle = 1

        hits = []

        x_locations = self.get_char_locations("M")

        for location in x_locations:
            letters_left = search_word[1:]
            check_distance = 1
            possible_directions = self.possible_directions_b(len(search_word), location)

            while len(letters_left) > 0 and len(possible_directions) > 0:
                # print(f"looking for {letters_left} from {location} in the following directions {self.possible_directions(location)} ")

                succesfull_directions = []
                for direction in possible_directions:
                    offset = tuple(x * check_distance for x in direction.value)
                    check_location = tuple(map(sum,zip(location,offset)))
                    
                    letter = self.lines[check_location[0]][check_location[1]]
                    
                    is_letter_correct = letter == letters_left[0]
                    # print(f"{check_location} -> {letter} {is_letter_correct}")

                    if is_letter_correct:
                        succesfull_directions.append(direction)

                possible_directions = succesfull_directions
                check_distance += 1
                letters_left = letters_left[1:]
            
            # print(letters_left)
            if letters_left == "":

                for direction in possible_directions:
                    offset = tuple(x * distance_to_middle for x in direction.value)
                    center_location = tuple(map(sum,zip(location,offset)))
                    hits.append(center_location)

        distinct_hits = list(set(hits))
        
        cross_hits = 0

        for distinct_hit in distinct_hits:
            if hits.count(distinct_hit) == 2:
                cross_hits += 1

        # print(hits)
        # print(cross_hits)
        return cross_hits
    
    def get_array_and_size(input) -> Tuple[List[str], int, int]:
        lines = input.split("\n")
        
        height = len(lines)
        width = len(lines[0])

        return lines, height, width


    def possible_directions_a(self, word_length, coordinate) -> List[Direction]:
        y_coord = coordinate[0]
        x_coord = coordinate[1]

        result = []

        if x_coord >= word_length - 1:
            result.append(Direction.W)
        if x_coord <= (self.width - word_length):
            result.append(Direction.E)

        if y_coord >= word_length - 1:
            result.append(Direction.N)
        if y_coord <= (self.height - word_length):
            result.append(Direction.S)


        if Direction.N in result and Direction.E in result:
            result.append(Direction.NE)
        if Direction.N in result and Direction.W in result:
            result.append(Direction.NW)
        if Direction.S in result and Direction.E in result:
            result.append(Direction.SE)
        if Direction.S in result and Direction.W in result:
            result.append(Direction.SW)
        
        return result
    
    def possible_directions_b(self, word_length, coordinate) -> List[Direction]:
        y_coord = coordinate[0]
        x_coord = coordinate[1]

        result = []

        if x_coord >= word_length - 1:
            result.append(Direction.W)
        if x_coord <= (self.width - word_length):
            result.append(Direction.E)

        if y_coord >= word_length - 1:
            result.append(Direction.N)
        if y_coord <= (self.height - word_length):
            result.append(Direction.S)

        new_result = []

        if Direction.N in result and Direction.E in result:
            new_result.append(Direction.NE)
        if Direction.N in result and Direction.W in result:
            new_result.append(Direction.NW)
        if Direction.S in result and Direction.E in result:
            new_result.append(Direction.SE)
        if Direction.S in result and Direction.W in result:
            new_result.append(Direction.SW)
        
        return new_result