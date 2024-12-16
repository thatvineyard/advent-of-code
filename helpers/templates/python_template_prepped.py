from ast import Set
from enum import Enum
from typing import List, Tuple
from libraries.solution_manager import PuzzleSolution

class Element:
    def __init__(self, character):
        self.character = character
        
    def __repr__(self):
        return f"({self.character})"

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
    def __init__(self, character, location: Vector):
        super().__init__(character)
        self.location = location
        
    def __repr__(self):
        return f"({super().__repr__}@{self.location})"

class Grid:
    def __init__(self, width: int, height: int, elements: List[GridElement] = []):
        self.width = width
        self.height = height
        self.element_map: Set[Vector, GridElement] = {}
        for element in elements:
            self.add_element(element)

    def add_element(self, element: GridElement):
        if element.location in self.element_map:
            raise KeyError(f"An element ({self.element_map[element.location]}) is already placed at {element.location}")

        self.element_map[element.location] = element

    def move_element(self, element: GridElement, new_location: Vector) -> GridElement:
        if new_location in self.element_map:
            raise KeyError(f"Tried to move element ({element}) to location ({new_location}) but another element ({self.element_map[element.location]}) is already there")
        if self.element_map[element.location] != element:
            raise RuntimeError(f"Elements ({element}) location did not match grid's element map")

        old_location = element.location
        self.element_map[old_location] = None
        element.location = new_location
        self.add_element(element)
        return element


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
        # for element in elements:
        #     print(element)
        
        # grid, elements = self.get_grid_elements(input)
        # print(grid)
        
        return ""

    def get_answer_b(self, input: str) -> int | float | str:
        return ""

    def get_row_elements(self, input: str) -> List[Element]:
        lines = input.split("\n")
        
        elements: List[Element] = []
        
        for line in lines:
            elements.append(Element(line[0]))
            
        return elements
        
    @staticmethod
    def get_grid_elements(input: str) -> Tuple[Grid, List[Element]]:
        lines = input.split("\n")
        
        grid = Grid(height=len(lines), width=len(lines[0]))
        
        elements: List[Element] = []
        
        for coordinate in grid.each_coordinate():
            character = lines[coordinate.y][coordinate.x]
            elements.append(Element(character=character))
            
        return grid, elements
        
