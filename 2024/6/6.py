from enum import Enum
from turtle import pos
from typing import List, Set, Tuple
from libraries.solution_manager import PuzzleSolution


class Direction(Enum):
    UP = ("^", (0, -1))
    RIGHT = (">", (1, 0)) 
    DOWN = ("v", (0, 1)) 
    LEFT = ("v", (-1, 0)) 

class Guard:

    def __init__(self, char, position: Tuple[int, int]):
        for direction in Direction:
            if char == direction.value[0]:
                self.direction = direction
        if self.direction == None:
            raise Exception("No direction")

        self.position = position

    def is_guard_char(char):
        for direction in Direction:
            if char == direction.value[0]:
                return True
        
        return False

    def rotate(self):
        self.direction = self.rotate_direction(self.direction)

    @staticmethod
    def rotate_direction(current_direction):
        match current_direction:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

    def move(self):
        self.position = self.get_target_coordinate()

    def get_target_coordinate(self):
        return tuple(map(sum, zip(self.position, self.direction.value[1])))

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        guard, barriers, width, height = Solution.get_elements(input)
        

        iteration = 0

        visited_positions = set()
        visited_positions.add(guard.position)

        while(not self.outside_map(guard.get_target_coordinate(), width, height)):
            iteration += 1
            if iteration > 100000:
                raise Exception("Too many iterations")


            if guard.get_target_coordinate() in barriers:
                guard.rotate()
                continue

            if guard.get_target_coordinate() not in barriers:
                guard.move()
                visited_positions.add(guard.position)


        return len(visited_positions)

    def get_answer_b(self, input: str) -> int | float | str:
        guard, barriers, width, height = Solution.get_elements(input)
        
        iteration = 0

        visited_positions_and_direction: Set[Tuple[Tuple[int, int], Direction]] = set()
        visited_positions_and_direction.add((guard.position, guard.direction))

        looping_barrier_positions = set()

        while(not self.outside_map(guard.get_target_coordinate(), width, height)):
            iteration += 1
            if iteration > 100000:
                raise Exception("Too many iterations")

            if not self.has_been_here(guard, visited_positions_and_direction) and guard.get_target_coordinate() not in looping_barrier_positions:
                if self.check_loop(guard, barriers, guard.get_target_coordinate(), width, height, visited_positions_and_direction):
                    looping_barrier_positions.add(guard.get_target_coordinate())


            if guard.get_target_coordinate() in barriers:
                guard.rotate()
                continue

            if guard.get_target_coordinate() not in barriers:
                guard.move()   
                current_position_and_direction = (guard.position, guard.direction)
                if current_position_and_direction in visited_positions_and_direction:
                    pass # LOOPED
                visited_positions_and_direction.add((guard.position, guard.direction))


        return len(looping_barrier_positions)

    def has_been_here(self, guard: Guard, visited_positions_and_direction):
        for position_and_direction in visited_positions_and_direction:
            if guard.get_target_coordinate() == position_and_direction[0]:
                return True
        return False


    def check_loop(self, guard: Guard, barriers: List[Tuple[int, int]], extra_barrier: Tuple[int, int], width: int, height:int, visited_positions: Set[Tuple[Tuple[int, int], Direction]]):
        visited_positions_copy = set(visited_positions)
        guard_copy = Guard(guard.direction.value[0], guard.position)

        iteration = 0
        while(not self.outside_map(guard_copy.get_target_coordinate(), width, height)):
            iteration += 1
            if iteration > 100000:
                raise Exception("Too many iterations")


            if guard_copy.get_target_coordinate() in barriers or guard_copy.get_target_coordinate() == extra_barrier:
                guard_copy.rotate()
                continue

            if guard_copy.get_target_coordinate() not in barriers and guard_copy.get_target_coordinate() != extra_barrier:
                guard_copy.move()   
                current_position_and_direction = (guard_copy.position, guard_copy.direction)
                if current_position_and_direction in visited_positions_copy:
                    return True
                visited_positions_copy.add(current_position_and_direction)

        return False

    @staticmethod
    def outside_map(target_coordinate, width, height):
        return target_coordinate[0] >= width or target_coordinate[0] < 0 or target_coordinate[1] >= height or target_coordinate[1] < 0


    def get_elements(input) -> Tuple[Guard, List[Tuple[int, int]], int, int]:
        lines = input.split("\n")

        height = len(lines)
        width = len(lines[0])
        
        barriers: List[Tuple[int, int]] = []

        for y in range(height):
            for x in range(width):
                char = lines[y][x]
                if Guard.is_guard_char(char):
                    guard = Guard(char, (x, y))
                if char == "#":
                    barriers.append((x, y))
                

        return (guard, barriers, width, height)