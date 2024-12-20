from ast import Set
from enum import Enum
import sys
from typing import Dict, List, Tuple
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
        return f"{self.x},{self.y}"

    def __eq__(self, value):
        if not isinstance(value, Vector):
            raise NotImplementedError(
                f"Tried to perform equals check on {Vector.__name__} ({self}) with something that's not a {Vector.__name__} ({value})"
            )
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return self.__repr__().__hash__()

    def zero():
        return Vector(0, 0)

class Direction(Enum):
    UP = ("^", Vector(0, -1))
    RIGHT = (">", Vector(1, 0)) 
    DOWN = ("v", Vector(0, 1)) 
    LEFT = ("<", Vector(-1, 0)) 

    def __repr__(self):
        return self.value[0]
    
    def is_opposite(self, other):
        return self.value[1] + other.value[1] == Vector.zero()

    
class GridElement(Element):
    def __init__(self, character, location: Vector):
        super().__init__(character)
        self.location = location
        
    def __repr__(self):
        return f"({super().__repr__()}@{self.location})"
    
    def short_name(self):
        return self.character

class EmptySpace(GridElement):
    def __init__(self, location: Vector):
        super().__init__(".", location)
        self.lowest_cost = sys.maxsize
        self.final_cost = sys.maxsize

    def short_name(self):        
        return super().short_name()

    def update_final_cost_if_lower(self, new_cost: int):
        if new_cost < self.final_cost:
            self.final_cost = new_cost

    def update_lowest_cost_if_lower(self, new_cost: int):
        if new_cost < self.final_cost:
            self.final_cost = new_cost

class Robot(GridElement):
    def __init__(self, location):
        super().__init__("X", location)

class Goal(GridElement):
    def __init__(self, location):
        super().__init__("E", location)

class Byte(EmptySpace):
    def __init__(self, location: Vector, turn: int):
        super().__init__(location)
        self.character = ","
        self.turn = turn
        self.corrupted = False

    def short_name(self, current_turn: int = -1):
        turns_until_corrupted = self.turn - current_turn
        if turns_until_corrupted <= 0:
            return "#"
        elif turns_until_corrupted < 10:
            return str(turns_until_corrupted)
        else:
            return self.character

    def is_corrupted(self, current_turn: int):
        turns_until_corrupted = self.turn - current_turn
        return turns_until_corrupted < 0

    def __repr__(self):
        return f"({self.turn}@{self.location})"
    
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

    def fill_with_empty_spaces(self):
        for coordinate in self.each_coordinate():
            if coordinate not in self.element_map:
                self.add_element(EmptySpace(coordinate))

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
    
    def try_get_at_location(self, location: Vector) -> GridElement | None:
        if location not in self.element_map:
            return None
        
        return self.element_map[location]
    
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

class ByteGrid(Grid):
    def __init__(self, width, height, elements = []):
        super().__init__(width, height, elements)
        self.turn = 0

    def __repr__(self):
        result = ""
        current_y_coord = 0
        for coordinate in self.each_coordinate():
            if current_y_coord != coordinate.y:
                result += "\n"
                current_y_coord = coordinate.y
            if coordinate in self.element_map:
                element = self.element_map[coordinate]  
                if isinstance(element, Byte):
                    result += self.element_map[coordinate].short_name(self.turn)
                else:
                    result += element.short_name()  
            else:
                result += "."
        return result

    def get_possible_directions_and_positions(self, location: Vector, turn: int) -> Dict[Direction, Vector]:
        result: Dict[Direction, Vector] = {}
        for direction in Direction:
            neighbor_coordinate = location + direction.value[1]
            
            if not self.is_in_bounds(neighbor_coordinate):
                continue
            
            if neighbor_coordinate not in self.element_map:
                raise Exception("Tried accessing a coordinate that is not in the element map")

            element = self.element_map[neighbor_coordinate]
            
            if isinstance(element, Byte):
                if not element.is_corrupted(turn):
                    result[direction] = neighbor_coordinate
                continue
       
            if isinstance(element, (EmptySpace, Goal)):
                result[direction] = neighbor_coordinate
                continue
       
        return result


    def find_best_path(self, from_position: Vector, current_direction: Direction, current_cost: int, turn: int, current_cheapest: int = sys.maxsize) -> Tuple[List[EmptySpace | Byte | Goal], int] | None:        
        lowest_cost_path = None

        for possible_direction, possible_location in self.get_possible_directions_and_positions(from_position, turn).items():
            if possible_direction.is_opposite(current_direction):
                continue

            element_at_location = self.try_get_at_location(possible_location)
            
            if not isinstance(element_at_location, (EmptySpace, Goal, Byte)):
                raise Exception(f"Expected element at location to be an empty space, goal, byte but was {type(element_at_location)}")
            
            if isinstance(element_at_location, Byte):
                if element_at_location.is_corrupted(turn):
                    raise Exception(f" {element_at_location.location}")
            
            cost_after_step = current_cost + 1
            if cost_after_step > current_cheapest:
                continue
            
            if isinstance(element_at_location, Goal):
                return ([element_at_location], cost_after_step)
            
            if element_at_location.lowest_cost <= cost_after_step:
                continue

            element_at_location.lowest_cost = cost_after_step

            if lowest_cost_path is not None:
                current_cheapest = lowest_cost_path[1]
            
            possible_path = self.find_best_path(possible_location, possible_direction, cost_after_step, turn, current_cheapest)

            if possible_path is not None:
                possible_path[0].append(element_at_location)
                element_at_location.update_final_cost_if_lower(possible_path[1])
                
                if lowest_cost_path is None:
                    lowest_cost_path = possible_path
                    continue

                if possible_path[1] < lowest_cost_path[1]:
                    lowest_cost_path = possible_path

        return lowest_cost_path

    def find_any_path(self, from_position: Vector, current_direction: Direction, current_cost: int, turn: int) -> Tuple[List[EmptySpace | Byte | Goal], int] | None:        
        for possible_direction, possible_location in self.get_possible_directions_and_positions(from_position, turn).items():
            if possible_direction.is_opposite(current_direction):
                continue

            element_at_location = self.try_get_at_location(possible_location)
            
            if not isinstance(element_at_location, (EmptySpace, Goal, Byte)):
                raise Exception(f"Expected element at location to be an empty space, goal, byte but was {type(element_at_location)}")
            
            if isinstance(element_at_location, Byte):
                if element_at_location.is_corrupted(turn):
                    raise Exception(f" {element_at_location.location}")
            
            cost_after_step = current_cost + 1
                        
            if isinstance(element_at_location, Goal):
                return ([element_at_location], cost_after_step)
            
            if element_at_location.lowest_cost <= cost_after_step:
                continue

            element_at_location.lowest_cost = cost_after_step
            
            possible_path = self.find_any_path(possible_location, possible_direction, cost_after_step, turn)

            # print(f"{from_position} -> {possible_location} {possible_path}")

            if possible_path is not None:
                possible_path[0].append(element_at_location)
                return possible_path

        return None

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        grid, robot, goal, turn, bytes = self.get_grid_elements(input)
        grid.turn = turn
        print(grid)
        print(robot)
        
        
        result = grid.find_best_path(from_position=robot.location, current_direction=Direction.RIGHT, current_cost=0, turn=turn)

        print(result)
        
        return result[1]

    def get_answer_b(self, input: str) -> int | float | str:
        grid, robot, goal, start_turn, bytes = self.get_grid_elements(input)
        # grid.turn = turn
        print(grid)
        print(robot)
        
        sys.setrecursionlimit(100000)
        
        turn = start_turn
        
        while turn < len(bytes):
            grid.turn = turn
            for element in grid.each_element():
                if isinstance(element, EmptySpace):
                    element.lowest_cost = sys.maxsize
                    element.final_cost = sys.maxsize
            
            result = grid.find_best_path(from_position=robot.location, current_direction=Direction.RIGHT, current_cost=0, turn=turn)

            if result == None:
                print(f"{turn}: None!")
                return str(bytes[turn - 1].location)
            else:
                print(f"{turn}: found path :(")

            next_turn = sys.maxsize
            for space in result[0]:
                if isinstance(space, Byte):
                    print(space)
                    if space.turn < next_turn:
                        next_turn = space.turn + 1

            turn = next_turn

        
    @staticmethod
    def get_grid_elements(input: str) -> Tuple[ByteGrid, Robot, Goal, int, List[Byte]]:
        lines = input.split("\n")
        
        test_input = len(lines) == 25
            
        if test_input:
            grid = ByteGrid(height=7, width=7)
            turn = 12
        else:
            grid = ByteGrid(height=71, width=71)
            turn = 1024
        
        bytes = []
        
        for line_i in range(len(lines)):
            x, y = lines[line_i].split(",")
            new_byte = Byte(location=Vector(int(x), int(y)), turn=line_i)
            grid.add_element(new_byte)
            bytes.append(new_byte)
        
        robot = Robot(location=Vector(0, 0))
        grid.add_element(robot)
        goal = Goal(location=Vector(grid.height-1, grid.width-1))
        grid.add_element(goal)
        
        grid.fill_with_empty_spaces()

        return grid, robot, goal, turn, bytes
        
