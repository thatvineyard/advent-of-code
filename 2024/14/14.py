import os
import time
from turtle import pos
from typing import List, Tuple
from libraries.solution_manager import PuzzleSolution


class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented(
                f"Tried adding coordinate ({self}) with something that's not a coodinate ({other})"
            )

        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented(
                f"Tried to perform subtraction on coordinate ({self}) with something that's not a coodinate ({other})"
            )

        return Vector(self.x - other.x, self.y - other.y)

    def scale(self, scale: int):
        return Vector(self.x * scale, self.y * scale)
    
    def __repr__(self):
        return f"{self.x},{self.y}"

    def __eq__(self, value):
        if not isinstance(value, Vector):
            raise NotImplemented(
                f"Tried to perform equals check on coordinate ({self}) with something that's not a coodinate ({value})"
            )
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return self.__repr__().__hash__()

    def zero():
        return Vector(0, 0)
    
    def one():
        return Vector(1, 1)

class Robot:
    def __init__(self, position: Vector, velocity: Vector):
        self.position = position
        self.velocity = velocity
        
    def __repr__(self):
        return f"(p={self.position} v={self.velocity}]"

    
class Grid:
    def __init__(self, width, height, origin = Vector(0,0)):
        self.width = width
        self.height = height
        self.origin = origin

    def __repr__(self):
        return f"({self.width}x{self.height}@{self.origin})"
    
    def __hash__(self):
        return hash(self.width) + hash(self.height) + hash(self.origin)

    def is_in_bounds(self, coordinate: Vector) -> bool:
        relative_coordinate = coordinate - self.origin
        return relative_coordinate.x < self.width and relative_coordinate.x >= 0 and relative_coordinate.y < self.height and relative_coordinate.y >= 0
    
    def each_coordinate(width, height):
        for y in range(height):
            for x in range(width):
                yield Vector(x, y)

    def calculate_wrapped_position(self, position: Vector, coordinate: Vector):
        new_position = position + coordinate
        new_position.x = new_position.x % self.width
        new_position.y = new_position.y % self.height
        return new_position

    def count_robots_in_quadrants(self, robots: List[Robot]):
        quadrant_TL = Grid(self.width // 2, self.height // 2, Vector.zero())
        quadrant_TR = Grid(self.width // 2, self.height // 2, Vector((self.width // 2) + 1, 0))
        quadrant_BL = Grid(self.width // 2, self.height // 2, Vector(0, (self.height // 2) + 1))
        quadrant_BR = Grid(self.width // 2, self.height // 2, Vector((self.width // 2) + 1, (self.height // 2) + 1))

        quadrant_counts = {quadrant_TL: 0, quadrant_TR: 0, quadrant_BL: 0, quadrant_BR: 0}

        for quadrant in quadrant_counts.keys():
            # print(f"{quadrant} ------")
            for robot in robots:
                if quadrant.is_in_bounds(robot.position):
                    # print(f"{robot} was in bounds")
                    quadrant_counts[quadrant] += 1

        return quadrant_counts

    def print_with_robots(self, robots: List[Robot]):
        for height_i in range(self.height):
            for width_i in range(self.width):
                robot_found = False
                for robot in robots:
                    if robot.position == Vector(width_i, height_i):
                        robot_found = True
                        break
                if robot_found:
                    print("X", end="")
                else:
                    print(".", end="")
            print()

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        grid, robots = self.get_row_elements(input)
        
        
        # for robot in robots:
        #     print(robot)
        
        # print("========")

        for step_i in range(100):
            for robot in robots:
                robot.position = grid.calculate_wrapped_position(robot.position, robot.velocity)



        # for robot in robots:
        #     print(robot)
        
        # print("========")



        quadrant_counts = grid.count_robots_in_quadrants(robots)

        product = 1

        for quadrant, count in quadrant_counts.items():
            # print(f"{quadrant}: {count}")
            product = product * count

        return product

    def get_answer_b(self, solution_input: str) -> int | float | str:
        grid, robots = self.get_row_elements(solution_input)
        
        
        # for robot in robots:
        #     print(robot)
        
        # print("========")

        for step_i in range(100, 200):
            for robot in robots:
                robot.position = grid.calculate_wrapped_position(robot.position, robot.velocity)
            print(f"================= {step_i} seconds ==================")
            grid.print_with_robots(robots)

            time.sleep(0.2)


        # for robot in robots:
        #     print(robot)
        
        # print("========")



        quadrant_counts = grid.count_robots_in_quadrants(robots)

        product = 1

        for quadrant, count in quadrant_counts.items():
            # print(f"{quadrant}: {count}")
            product = product * count

        return product

    def get_row_elements(self, input: str) -> Tuple[Grid, List[Robot]]:
        lines = input.split("\n")
        
        if len(lines) < 15:
            grid = Grid(11, 7)
        else:
            grid = Grid(101, 103)

        robots: List[Robot] = []
        
        for line in lines:
            line_parts = line.split(" ")
            position_parts = line_parts[0].split("=")[1].split(",")
            position = Vector(int(position_parts[0]), int(position_parts[1]))
            velocity_parts = line_parts[1].split("=")[1].split(",")
            velocity = Vector(int(velocity_parts[0]), int(velocity_parts[1]))
            robots.append(Robot(position, velocity))
            
        return grid, robots
