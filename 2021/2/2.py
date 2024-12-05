from enum import Enum
from libraries.solution_manager import PuzzleSolution

class Directions(Enum):
    FORWARD = (1, 0)
    DOWN = (0, 1)
    UP = (0, -1)

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        
        orders = input.split("\n")

        position = (0, 0)

        for order in orders:
            [direction, amount] = order.split(" ")

            for possible_direction in Directions:
                if direction.capitalize() == possible_direction.name.capitalize():
                    scaled_direction = tuple([int(amount) * x for x in possible_direction.value])
                    position = tuple(map(sum, zip(position, scaled_direction)))
        
        return position[0] * position[1]


    def get_answer_b(self, input: str) -> int | float | str:
        
        orders = input.split("\n")

        aim = 0
        position = (0, 0)

        for order in orders:
            [direction, amount] = order.split(" ")

            for possible_direction in Directions:
                
                if direction.capitalize() == possible_direction.name.capitalize():
                    scaled_direction = tuple([int(amount) * x for x in possible_direction.value])
                    aim += scaled_direction[1]
                    position = tuple(map(sum, zip(position, (scaled_direction[0], scaled_direction[0]*aim))))
        
        return position[0] * position[1]