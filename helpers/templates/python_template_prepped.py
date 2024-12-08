from typing import List, Tuple
from libraries.solution_manager import PuzzleSolution

class Element:
    def __init__(self, character):
        self.character = character
        
    def __repr__(self):
        return f"[{self.character}]"

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Coordinate):
            raise NotImplemented(
                f"Tried adding coordinate ({self}) with something that's not a coodinate ({other})"
            )

        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Coordinate):
            raise NotImplemented(
                f"Tried to perform subtraction on coordinate ({self}) with something that's not a coodinate ({other})"
            )

        return Coordinate(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    def __eq__(self, value):
        if not isinstance(value, Coordinate):
            raise NotImplemented(
                f"Tried to perform equals check on coordinate ({self}) with something that's not a coodinate ({other})"
            )
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return self.__repr__().__hash__()

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def is_in_bounds(self, coordinate: Coordinate) -> bool:
        return coordinate.x < self.width and coordinate.x >= 0 and coordinate.y < self.height and coordinate.y >= 0
    
    def each_coordinate(width, height):
        for y in range(height):
            for x in range(width):
                yield Coordinate(x, y)

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        elements = self.get_row_elements(input)
        # grid, elements = self.get_grid_elements(input)
        
        for element in elements:
            print(element)
        
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
        
