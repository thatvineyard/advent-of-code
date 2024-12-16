from enum import Enum
import sys
from typing import Dict, List, Set, Tuple
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

class TraversalCost:
    def __init__(self, steps: int, turns: int):
        self.steps = steps
        self.turns = turns

    def cost(self):
        return self.steps + (self.turns * 1000)

    def __add__(self, other):
        if not isinstance(other, TraversalCost):
            raise NotImplementedError(
                f"Tried to perform addition on {TraversalCost.__name__} ({self}) with something that's not a {TraversalCost.__name__} ({other})"
            )

        return TraversalCost(self.steps + other.steps, self.turns + other.turns)

    def __lt__(self, other):
        if not isinstance(other, TraversalCost):
            raise NotImplementedError(
                f"Tried to perform gt check on {TraversalCost.__name__} ({self}) with something that's not a {TraversalCost.__name__} ({other})"
            )
        
        return self.cost() < other.cost()
    
    def __gt__(self, other):
        if not isinstance(other, TraversalCost):
            raise NotImplementedError(
                f"Tried to perform gt check on {TraversalCost.__name__} ({self}) with something that's not a {TraversalCost.__name__} ({other})"
            )
        
        return self.cost() > other.cost()

    def __eq__(self, other):
        if not isinstance(other, TraversalCost):
            raise NotImplementedError(
                f"Tried to perform equals check on {TraversalCost.__name__} ({self}) with something that's not a {TraversalCost.__name__} ({other})"
            )
        
        return self.cost() == other.cost()
    
    def __repr__(self):
        return f"({self.steps}x{self.turns}={self.cost()})"


class GridElement(Element):
    def __init__(self, character, location: Vector):
        super().__init__(character)
        self.location = location
        
    def __repr__(self):
        return f"({super().__repr__()}@{self.location})"


class EmptySpace(GridElement):
    def __init__(self, location: Vector):
        super().__init__(".", location)
        self.lowest_cost_per_direction: Dict[Direction, TraversalCost] = {}
        self.final_cost = TraversalCost(sys.maxsize, sys.maxsize)
        self.is_on_best_path = False

    def set_cost(self, direction: Direction, cost: TraversalCost):
        self.lowest_cost_per_direction[direction] = cost
    
    def short_name(self):
        if len(self.lowest_cost_per_direction.items()) == 0:
            return super().short_name()

        if self.is_on_best_path:
            return "0"

        if len(self.lowest_cost_per_direction.items()) == 1:
            return str(list(self.lowest_cost_per_direction.keys())[0].value[0])
           
        if len(self.lowest_cost_per_direction.items()) == 2:
            return "X"
           
        if len(self.lowest_cost_per_direction.items()) == 3:
            return "*"
        
        return super().short_name()

    def update_final_cost_if_lower(self, new_cost: TraversalCost):
        if new_cost < self.final_cost:
            self.final_cost = new_cost

class Wall(GridElement):
    def __init__(self, location: Vector):
        super().__init__("#", location)

class Robot(GridElement):
    def __init__(self, location: Vector, direction: Direction):
        super().__init__("S", location)
        self.direction = direction

    def short_name(self):
        return self.direction.value[0]
    

class Goal(GridElement):
    def __init__(self, location: Vector):
        super().__init__("E", location)

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

    def try_get_at_location(self, location: Vector) -> GridElement | None:
        if location not in self.element_map:
            return None
        
        return self.element_map[location]

    def get_possible_directions_and_positions(self, location: Vector) -> Dict[Direction, Vector]:
        result: Dict[Direction, Vector] = {}
        for direction in Direction:
            next_location = location + direction.value[1]
            if next_location not in self.element_map:
                continue

            if isinstance(self.element_map[next_location], Wall):
                continue

            result[direction] = next_location
        
        return result

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
                result += " "
        return result

    def find_best_path(self, from_position: Vector, current_direction: Direction, to_position: Vector, current_cost: TraversalCost, current_cheapest: TraversalCost = TraversalCost(sys.maxsize, sys.maxsize)) -> Tuple[List[EmptySpace | Goal], TraversalCost] | None:        
        lowest_cost_path = None

        for possible_direction, possible_location in self.get_possible_directions_and_positions(from_position).items():
            if possible_direction.is_opposite(current_direction):
                continue

            element_at_location = self.try_get_at_location(possible_location)
            
            if not isinstance(element_at_location, (EmptySpace, Goal, Robot)):
                raise Exception(f"Expected element at location to be an empty space, goal or robot but was {type(element_at_location)}")
            
            if isinstance(element_at_location, Robot):
                continue
             
            if current_direction == possible_direction:
                cost_before_step = current_cost
            else:
                cost_before_step = current_cost + TraversalCost(0, 1)


            cost_after_step = cost_before_step + TraversalCost(1, 0)

            if cost_after_step > current_cheapest:
                continue

            if isinstance(element_at_location, Goal):
                print(f"Found goal with cost {cost_after_step}")
                return ([element_at_location], cost_after_step)
            

            if possible_direction in element_at_location.lowest_cost_per_direction:
                if element_at_location.lowest_cost_per_direction[possible_direction] < cost_after_step:
                    continue

            element_at_location.lowest_cost_per_direction[possible_direction] = cost_after_step

            if lowest_cost_path is not None:
                current_cheapest = lowest_cost_path[1]
            
            possible_path = self.find_best_path(possible_location, possible_direction, to_position, cost_after_step, current_cheapest)

            if possible_path is not None:
                possible_path[0].append(element_at_location)
                element_at_location.update_final_cost_if_lower(possible_path[1])
                
                # if isinstance(possible_path[0][0], Goal):
                #     lowest_cost_path = possible_path
                #     continue
                
                if lowest_cost_path is None:
                    lowest_cost_path = possible_path
                    continue


            
                if possible_path[1] < lowest_cost_path[1]:
                    lowest_cost_path = possible_path

        return lowest_cost_path
        

    # def find_best_paths(self, from_position: Vector, current_direction: Direction, to_position: Vector, current_cost: TraversalCost, current_cheapest: TraversalCost = TraversalCost(sys.maxsize, sys.maxsize)) -> Tuple[List[List[EmptySpace | Goal]], TraversalCost] | None:        
    #     lowest_cost_paths = []

    #     for possible_direction, possible_location in self.get_possible_directions_and_positions(from_position).items():
    #         if possible_direction.is_opposite(current_direction):
    #             continue

    #         element_at_location = self.try_get_at_location(possible_location)
            
    #         if not isinstance(element_at_location, (EmptySpace, Goal, Robot)):
    #             raise Exception(f"Expected element at location to be an empty space, goal or robot but was {type(element_at_location)}")
            
    #         if isinstance(element_at_location, Robot):
    #             return None
            
            
    #         if current_direction == possible_direction:
    #             cost_before_step = current_cost
    #         else:
    #             cost_before_step = current_cost + TraversalCost(0, 1)


    #         cost_after_step = cost_before_step + TraversalCost(1, 0)

    #         if cost_after_step > current_cheapest:
    #             return None

    #         if isinstance(element_at_location, Goal):
    #             print(f"Found goal with cost {cost_after_step}")
    #             return ([[element_at_location]], cost_after_step)
            

    #         if possible_direction in element_at_location.lowest_cost_per_direction:
    #             if element_at_location.lowest_cost_per_direction[possible_direction] < cost_after_step:
    #                 return None

    #         element_at_location.lowest_cost_per_direction[possible_direction] = cost_after_step

            
    #         possible_paths = self.find_best_paths(possible_location, possible_direction, to_position, cost_after_step, current_cheapest)


    #         if possible_paths is None:
    #             continue

    #         for possible_path in possible_paths[0]:
    #             possible_path.append(element_at_location)

    #             if isinstance(possible_path[0], Goal):
    #                 lowest_cost_paths.append(possible_path)
    #                 continue

    #             if possible_path[1] < current_cheapest:
    #                 lowest_cost_paths.append(possible_path)
    #                 current_cheapest = possible_path[1]
        
    #     if len(lowest_cost_paths) <= 0:
    #         return None
 
    #     return (lowest_cost_paths, current_cheapest)
        


class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        # elements = self.get_row_elements(input)
        # for element in elements:
        #     print(element)
        sys.setrecursionlimit(10000)
        
        grid, robot, goal = self.get_grid_elements(input)
        print(grid)
        print(robot)
        print(goal)
        

        path, cost = grid.find_best_path(robot.location, robot.direction, goal.location, TraversalCost(0, 0))

        print(cost)


        return cost.cost()

    def get_answer_b(self, input: str) -> int | float | str:
        sys.setrecursionlimit(30000)
        
        grid, robot, goal = self.get_grid_elements(input)
        print(grid)
        print(robot)
        print(goal)
        

        _, cost = grid.find_best_path(robot.location, robot.direction, goal.location, TraversalCost(0, 0))

        # spots: Set[Vector] = set()

        # for path in paths:
        #     for location in path:
        #         spots.add(location)

        sum = 2

        print(cost)

        for element in grid.each_element():
            if not isinstance(element, EmptySpace):
                continue

            if element.final_cost == cost:
                element.is_on_best_path = True
                sum += 1

        print(grid)
        return sum
        
    @staticmethod
    def get_grid_elements(input: str) -> Tuple[Grid, Robot, Goal]:
        lines = input.split("\n")
        
        grid = Grid(height=len(lines), width=len(lines[0]))
        
        for coordinate in grid.each_coordinate():
            character = lines[coordinate.y][coordinate.x]
            if character == "S":
                robot = Robot(coordinate, Direction.RIGHT)
                grid.add_element(robot)
                continue
            if character == "#":
                wall = Wall(coordinate)
                grid.add_element(wall)
                continue
            if character == "E":
                goal = Goal(coordinate)
                grid.add_element(goal)
                continue
            if character == ".":
                space = EmptySpace(coordinate)
                grid.add_element(space)
                continue
            
        if robot is None:
            raise Exception("No robot found")
        
        return grid, robot, goal
        
