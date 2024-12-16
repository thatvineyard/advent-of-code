from ast import Set
from enum import Enum
import time
from typing import Dict, List, Tuple
from libraries.solution_manager import PuzzleSolution



class Element:
    def __init__(self, character):
        self.character = character
        
    def __repr__(self):
        return f"({self.character})"
    
    def short_name(self):
        return self.character[0:1]

class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError(
                f"Tried adding {Vector.__name__} ({self}) with something that's not a {Vector.__name__} ({other})"
            )

        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError(
                f"Tried to perform subtraction on {Vector.__name__} ({self}) with something that's not a {Vector.__name__} ({other})"
            )

        return Vector(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, value):
        if not isinstance(value, Vector):
            raise NotImplementedError(
                f"Tried to perform equals check on {Vector.__name__} ({self}) with something that's not a {Vector.__name__} ({value})"
            )
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return self.__repr__().__hash__()

class Direction(Enum):
    UP = ("^", Vector(0, -1))
    RIGHT = (">", Vector(1, 0)) 
    DOWN = ("v", Vector(0, 1)) 
    LEFT = ("<", Vector(-1, 0)) 

    def __repr__(self):
        return self.value[0]

class GridElement(Element):
    def __init__(self, character, location: Vector, width = 1):
        super().__init__(character)
        self.location = location
        self.width = width

    def __repr__(self):
        return f"({super().__repr__()}@{self.location})"
    
class Wall(GridElement):
    def __init__(self, location: Vector, width = 1):
        super().__init__("#", location, width)
    
class Block(GridElement):
    def __init__(self, location: Vector, width = 1):
        super().__init__("O", location, width)

    def lantern_gps(self):
        return self.location.y * 100 + self.location.x
    
class Robot(GridElement):
    def __init__(self, location: Vector, width = 1):
        super().__init__("@", location, width)



class Grid:
    def __init__(self, width: int, height: int, elements: List[GridElement] = []):
        self.width = width
        self.height = height
        self.element_map: Dict[Vector, GridElement] = {}
        for element in elements:
            self.add_element(element)

    def add_element(self, element: GridElement):
        if element.location in self.element_map:
            raise KeyError(f"An element ({self.element_map[element.location]}) is already placed at {element.location}")

        self.element_map[element.location] = element

    def move_element_to(self, element: GridElement, new_location: Vector) -> GridElement:
        if new_location in self.element_map:
            raise KeyError(f"Tried to move element ({element}) to location ({new_location}) but another element ({self.element_map[element.location]}) is already there")
        if self.element_map[element.location] != element:
            raise RuntimeError(f"Elements ({element}) location did not match grid's element map")

        old_location = element.location
        del self.element_map[old_location]
        element.location = new_location
        self.add_element(element)
        return element

    def move_element(self, element: GridElement, direction: Direction):
        return self.move_element_to(element, element.location + direction.value[1])


    def get_contiguous_chain(self, location: Vector, direction: Direction):
        if location not in self.element_map:
            return []
        
        element_at_location = self.element_map[location] 
        
        if isinstance(element_at_location, Wall):
            return [element_at_location]

        next_location = location + direction.value[1]

        next_chain = self.get_contiguous_chain(next_location, direction)
        return [element_at_location] + next_chain 

    def is_in_bounds(self, coordinate: Vector) -> bool:
        return coordinate.x < self.width and coordinate.x >= 0 and coordinate.y < self.height and coordinate.y >= 0
    
    def each_coordinate(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Vector(x, y)

    def each_element(self):
        for element in self.element_map.values():
            yield element

    def __repr__(self):
        result = ""
        current_y_coord = 0
        for coordinate in self.each_coordinate():
            if current_y_coord != coordinate.y:
                result += "\n"
                current_y_coord = coordinate.y
            if coordinate in self.element_map:
                result += self.element_map[coordinate].short_name()
            else:
                result += "."
        return result


class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        # elements = self.get_row_elements(input)
        grid, robot, directions = self.get_grid_elements(input)
        
        print(grid)
        print(directions)

        for direction in directions:
            chain = grid.get_contiguous_chain(robot.location, direction)
            chain.reverse()
            if isinstance(chain[0], Wall):
                continue 
            for chain_part in chain:
                grid.move_element(chain_part, direction)

        sum = 0
        for element in grid.each_element():
            if isinstance(element, Block):
                sum += element.lantern_gps()

        return sum

    def get_answer_b(self, input: str) -> int | float | str:
        return ""
        
    @staticmethod
    def get_grid_elements(input: str) -> Tuple[Grid, Robot, List[Direction]]:
        blocks = input.split("\n\n")
        grid_lines = blocks[0].split("\n")
        
        grid = Grid(height=len(grid_lines), width=len(grid_lines[0]))
        
        robot = None

        for coordinate in grid.each_coordinate():
            character = grid_lines[coordinate.y][coordinate.x]

            if character == "#":
                grid.add_element(Wall(coordinate))
                continue
            if character == "O":
                grid.add_element(Block(coordinate))
                continue
            if character == "@":
                robot = Robot(coordinate)
                grid.add_element(robot)
                continue

        directions: List[Direction] = []

        directions_line = "".join(blocks[1].split("\n"))
        for direction_char in directions_line:
            for direction in Direction:
                if direction_char == direction.value[0]:
                    directions.append(direction)

        return grid, robot, directions
        
    @staticmethod
    def get_grid_elements_part_b(input: str) -> Tuple[Grid, Robot, List[Direction]]:
        blocks = input.split("\n\n")
        grid_lines = blocks[0].split("\n")
        
        grid = Grid(height=len(grid_lines), width=len(grid_lines[0]))
        
        robot = None

        for coordinate in grid.each_coordinate():
            character = grid_lines[coordinate.y][coordinate.x]

            if character == "#":
                grid.add_element(Wall(coordinate))
                continue
            if character == "O":
                grid.add_element(Block(coordinate))
                continue
            if character == "@":
                robot = Robot(coordinate)
                grid.add_element(robot)
                continue

        directions: List[Direction] = []

        directions_line = "".join(blocks[1].split("\n"))
        for direction_char in directions_line:
            for direction in Direction:
                if direction_char == direction.value[0]:
                    directions.append(direction)

        return grid, robot, directions
        
