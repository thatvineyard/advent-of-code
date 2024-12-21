from enum import Enum
import sys
from typing import Dict, List, Set, Tuple

from sty import fg
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
        if other is None:
            return False
        return self.value[1] + other.value[1] == Vector.zero()

class GridElement(Element):
    def __init__(self, character, location: Vector):
        super().__init__(character)
        self.location = location
        
    def __repr__(self):
        return f"({super().__repr__}@{self.location})"

    
class GridElement(Element):
    def __init__(self, character, location: Vector):
        super().__init__(character)
        self.location = location
        
    def __repr__(self):
        return f"({super().__repr__()}@{self.location})"
    
    def short_name(self):
        return self.character
    
class Wall(GridElement):
    def __init__(self, location: Vector):
        super().__init__("#", location)
        self.cheat_cost = sys.maxsize

class PathElement(GridElement):
    def __init__(self, character: str, location: Vector):
        super().__init__(character, location)
        self.cost = sys.maxsize
    
    def update_cost_if_lower(self, new_cost: int):
        if new_cost < self.cost:
            self.cost = new_cost

class EmptySpace(PathElement):
    def __init__(self, location: Vector):
        super().__init__(".", location)

    def short_name(self):        
        return super().short_name()

class Start(PathElement):
    def __init__(self, location):
        super().__init__("S", location)

class Goal(PathElement):
    def __init__(self, location):
        super().__init__("E", location)
    

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
    
    def get_neighbor_elements(self, location: Vector) -> List[GridElement]:
        result: List[GridElement] = []
        for direction in Direction:
            element_at_direction = self.try_get_at_location(location + direction.value[1])
            
            if element_at_direction is not None:
                result.append(element_at_direction)
                
        return result

    def get_neighbor_elements_at_distance(self, location: Vector, distance: int) -> Dict[int, GridElement]:
        current_search_candidates = [location]
        touched: Set[GridElement] = set()
        touched.add(location)
        
        result_per_step: Dict[int, List[GridElement]] = {}
        
        for i in range(1, distance + 1):
            result_per_step[i] = []
            next_search_candidates = []
            for search_candidate in current_search_candidates:
                neighbors = self.get_neighbor_elements(search_candidate)
                for neighbor in neighbors:
                    if neighbor in touched:
                        # print(f"{neighbor} touched already")
                        continue
                    
                    next_search_candidates.append(neighbor.location)
                    touched.add(neighbor)
                    result_per_step[i].append(neighbor)
                
            current_search_candidates = next_search_candidates
        
        
        # for steps, result in result_per_step.items():
            # print(f"Found {len(result)} from {location} at distance {steps}")
        return result_per_step
    
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

class RaceGrid(Grid):
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
                result += element.short_name()  
            else:
                result += "."
        return result

    def get_possible_directions_and_positions(self, location: Vector) -> Dict[Direction, Vector]:
        result: Dict[Direction, Vector] = {}
        for direction in Direction:
            neighbor_coordinate = location + direction.value[1]
            
            if not self.is_in_bounds(neighbor_coordinate):
                continue
            
            if neighbor_coordinate not in self.element_map:
                raise Exception("Tried accessing a coordinate that is not in the element map")

            element = self.element_map[neighbor_coordinate]
                   
            if isinstance(element, PathElement):
                result[direction] = neighbor_coordinate
                continue
       
        return result

    def set_costs_for_spaces(self, from_position: Vector, current_direction: Direction, current_cost: int = 0):        
        element_at_current_location = self.try_get_at_location(from_position)
        if not isinstance(element_at_current_location, (PathElement)):
            raise Exception(f"Expected element at location to be a path element but was {type(element_at_current_location)}")
        
        element_at_current_location.update_cost_if_lower(current_cost)
        
        if isinstance(element_at_current_location, Goal):
            return
        
        for possible_direction, possible_location in self.get_possible_directions_and_positions(from_position).items():
            if possible_direction.is_opposite(current_direction):
                continue

            element_at_location = self.try_get_at_location(possible_location)
            if not isinstance(element_at_location, (PathElement)):
                raise Exception(f"Expected element at location to be a path element but was {type(element_at_current_location)}")
            
            cost_after_step = current_cost + 1
                        
            if element_at_location.cost <= cost_after_step:
                continue

            self.set_costs_for_spaces(possible_location, possible_direction, cost_after_step)
        return None

    def print_costs(self):
        result = ""
        current_y_coord = 0
        for coordinate in self.each_coordinate():
            if current_y_coord != coordinate.y:
                result += "\n"
                current_y_coord = coordinate.y
            if coordinate in self.element_map:
                element = self.element_map[coordinate]
                if isinstance(element, PathElement):
                    result += f"{fg.yellow}{str(element.cost % 10)}{fg.rs}"
                elif isinstance(element, Wall):
                    if element.cheat_cost == sys.maxsize:
                        result += f"{fg.black}X{fg.rs}"
                    else:
                        result += f"{fg.black}{element.cheat_cost % 10}{fg.rs}"
                else:
                    result += "."
            else:
                result += "."
        print(result)

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        grid, start, goal, walls, threshold = self.get_grid_elements(input)
        
        sys.setrecursionlimit(10000)
        
        grid.set_costs_for_spaces(from_position=start.location, current_direction=None)
        

        
        num_possible_wall_cheats = 0 
        num_good_cheats = 0
        num_bad_cheats = 0
        
        grid.print_costs()
        
        
        for element in grid.each_element():
            if not isinstance(element, Wall):
                continue
            
            path_neighbors = grid.get_neighbor_elements(element.location)
            
            min_neighbor_cost = None
            for neighbor in path_neighbors:
                if isinstance(neighbor, Wall):
                    if min_neighbor_cost is None:
                        min_neighbor_cost = neighbor.cheat_cost
                
                if isinstance(neighbor, PathElement):
                    if min_neighbor_cost is None:
                        min_neighbor_cost = neighbor.cost
                
            element.cheat_cost = min_neighbor_cost - 1
            
        grid.print_costs()
        
        return num_good_cheats

    @staticmethod
    def get_neighbor_pairs(neighbors: List[PathElement]) -> List[Tuple[PathElement, PathElement]]:
        pairs: List[Tuple[PathElement, PathElement]] = []
        
        handled_neighbors: List[PathElement] = []
        for neighbor in neighbors:
            handled_neighbors.append(neighbor)
            for other_neighbor in neighbors:
                if other_neighbor in handled_neighbors:
                    continue
                
                if neighbor.location.x == other_neighbor.location.x or neighbor.location.y == other_neighbor.location.y:
                    pairs.append((neighbor, other_neighbor))
                    
        return pairs
        
        
    def get_answer_b(self, input: str) -> int | float | str:
        grid, start, goal, walls, threshold = self.get_grid_elements(input)
        
        sys.setrecursionlimit(10000)
        
        grid.set_costs_for_spaces(from_position=start.location, current_direction=None)
        
        
        num_possible_wall_cheats = 0 
        num_good_cheats = 0
        num_bad_cheats = 0
        
        grid.print_costs()
        
        for element in grid.each_element():
            if not isinstance(element, PathElement):
                continue
            
            neighbors_per_step = grid.get_neighbor_elements_at_distance(element.location, 20)
            
            num_neighbors_looked_at = 0
            
            for step, neighbors in neighbors_per_step.items():
                num_neighbors_looked_at += len(neighbors)
                cost = element.cost + step
                
                neighbors: List[PathElement] = list(filter(lambda x: isinstance(x, PathElement), neighbors))
                
                neighbor_and_saved_cost: List[Tuple[PathElement, int]] = []
                
                for neighbor in neighbors:
                    saved_cost = neighbor.cost - cost
                    if 0 < saved_cost < threshold:
                        num_bad_cheats += 1
                    elif saved_cost >= threshold:
                        neighbor_and_saved_cost.append((neighbor, saved_cost))
                        
                # if len(neighbor_and_saved_cost) > 0:
                    # print(f"{element.location} {element.cost} -{step}-> {list(map(lambda x: (x[0].location, x[0].cost, x[1]), neighbor_and_saved_cost))}")
            
                num_good_cheats += len(neighbor_and_saved_cost)
        
            # print(f"Looked at {num_neighbors_looked_at} neighbors for {element}")
        
        print(num_possible_wall_cheats)
        print(num_bad_cheats)
        print(num_good_cheats)
        
        return num_good_cheats

    @staticmethod
    def get_grid_elements(input: str) -> Tuple[RaceGrid, Start, Goal, List[Wall]]:
        lines = input.split("\n")
        
        grid = RaceGrid(height=len(lines), width=len(lines[0]))
        
        if len(lines) < 16:
            threshold = 72
            # threshold = 20
        else:
            threshold = 100
        
        walls: List[Wall] = []
        
        for coordinate in grid.each_coordinate():
            character = lines[coordinate.y][coordinate.x]
            match character:
                case "#":
                    new_wall = Wall(coordinate)
                    grid.add_element(new_wall)
                    walls.append(new_wall)
                case ".":
                    grid.add_element(EmptySpace(coordinate))
                case "S":
                    start = Start(coordinate)
                    grid.add_element(start)
                case "E":
                    goal = Goal(coordinate)
                    grid.add_element(goal)
                case _:
                    raise ValueError("Unexpected character")
            
        return grid, start, goal, walls, threshold
        
