from typing import Callable, Dict, List, Tuple

from libraries.solution_manager import PuzzleSolution


class Elevation:
    def __init__(self, height: int):
        self.height = height
        
    def __repr__(self):
        return f"[{self.height}]"

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def each_surrounding_coordinate(self):
        yield Coordinate(self.x + 0, self.y + 1)
        yield Coordinate(self.x + 1, self.y + 0)
        yield Coordinate(self.x + 0, self.y - 1)
        yield Coordinate(self.x - 1, self.y + 0)

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
                f"Tried to perform equals check on coordinate ({self}) with something that's not a coodinate ({value})"
            )
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return self.__repr__().__hash__()


class TraversalNode:
    def __init__(self, elevation: Elevation, location: Coordinate):
        self.elevation = elevation
        self.location = location
        self.parent_node: TraversalNode = None
        self.child_nodes: List[TraversalNode] = []

    def add_node(self, node):
        if not isinstance(node, TraversalNode):
            raise NotImplemented(
                "Tried to add object that was not a node"
            )
        
        node.parent_node = self
        self.child_nodes.append(node)


    
    

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.elements: Dict[Coordinate, Elevation] = {}
    
    def is_in_bounds(self, coordinate: Coordinate) -> bool:
        return coordinate.x < self.width and coordinate.x >= 0 and coordinate.y < self.height and coordinate.y >= 0
    
    def place_element(self, element: Coordinate, location: Coordinate):
        self.elements[location] = element

    def each_coordinate(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Coordinate(x, y)

    def each_element(self):
        for coordinate in self.each_coordinate():
            yield self.try_get_element(coordinate)

    def try_get_element(self, location: Coordinate) -> Elevation:
        if location in self.elements:
            return self.elements[location]
        else:
            return None

    def each_row(self):
        for y in range(self.height):
            yield [Coordinate(x, y) for x in range(self.width)]

    def each_element_row(self):
        for row in self.each_row():
            yield list(map(self.try_get_element, row))

    def __repr__(self):
        result = ""
        for row in self.each_element_row():
            result += str(row) + "\n"
        return result
    
    def get_element_by_comparison(self, compare_function: Callable[[Elevation, Elevation], bool]) -> Elevation:
        current = None
        
        for element in self.each_element():
            if current is None:
                current = element
                continue

            if compare_function(element, current):
                current = element
                continue

        return current
    
    def get_elements_that_match(self, filter_function: Callable[[Elevation], bool]) -> List[Tuple[Elevation, Coordinate]]:
        result = []

        for coordinate in self.each_coordinate():
            element = self.try_get_element(coordinate)
            if filter_function(element):
                result.append((element, coordinate))


        return result



    def get_highest(self):
        return self.get_element_by_comparison(lambda x, y: x.height > y.height)
    
    def get_lowest(self):
        return self.get_element_by_comparison(lambda x, y: x.height < y.height)

    def get_neighbors(self, location: Coordinate) -> List[Tuple[Elevation, Coordinate]]:
        result = []
        for surrounding_coordinate in location.each_surrounding_coordinate():
            element = self.try_get_element(surrounding_coordinate)
            if element is not None:
                result.append((element, surrounding_coordinate))
        
        return result


class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        # elements = self.get_row_elements(input)
        grid, elements = self.get_grid_elements(input)
        highest_elevation = grid.get_highest()
        lowest_elevation = grid.get_lowest()
        
        # print(grid)
        all_highest_points: List[Tuple[Elevation, Coordinate]] = grid.get_elements_that_match(lambda x: x.height == highest_elevation.height)
        all_lowest_points: List[Tuple[Elevation, Coordinate]] = grid.get_elements_that_match(lambda x: x.height == lowest_elevation.height)
        
        
        sum = 0

        for point in all_lowest_points:
            # print(point)
            node = TraversalNode(point[0], point[1])
            result_nodes = self.traverse_to_top(node, grid, highest_elevation)
            
            unique_positions = set()

            for result_node in result_nodes:
                unique_positions.add(result_node.location)
            
            # print(len(unique_positions))
            sum += len(unique_positions)

        
        # print(lowest_elevation)
        
        return sum
    
    def traverse_to_top(self, node: TraversalNode, grid: Grid, max_elevation: Elevation) -> List[TraversalNode]:
        neighbors = grid.get_neighbors(node.location)
        result: List[TraversalNode] = []
        
        # print(f"{node.location}: {node.elevation}")

        if node.elevation.height == max_elevation.height:
            result.append(node)
        for neighbor in neighbors:
            if neighbor[0].height == node.elevation.height + 1:
                new_node = TraversalNode(neighbor[0], neighbor[1])
                nodes = self.traverse_to_top(new_node, grid, max_elevation)
                result += nodes

        return result



    def get_answer_b(self, input: str) -> int | float | str:
        # elements = self.get_row_elements(input)
        grid, elements = self.get_grid_elements(input)
        highest_elevation = grid.get_highest()
        lowest_elevation = grid.get_lowest()
        
        # print(grid)
        all_highest_points: List[Tuple[Elevation, Coordinate]] = grid.get_elements_that_match(lambda x: x.height == highest_elevation.height)
        all_lowest_points: List[Tuple[Elevation, Coordinate]] = grid.get_elements_that_match(lambda x: x.height == lowest_elevation.height)
        
        
        sum = 0

        for point in all_lowest_points:
            # print(point)
            node = TraversalNode(point[0], point[1])
            result_nodes = self.traverse_to_top(node, grid, highest_elevation)
            
            # unique_positions = set()

            # for result_node in result_nodes:
            #     unique_positions.add(result_node.location)
            
            # print(len(unique_positions))
            sum += len(result_nodes)

        
        # print(lowest_elevation)
        
        return sum

    def get_row_elements(self, input: str) -> List[Elevation]:
        lines = input.split("\n")
        
        elements: List[Elevation] = []
        
        for line in lines:
            elements.append(Elevation(line[0]))
            
        return elements
        
    @staticmethod
    def get_grid_elements(input: str) -> Tuple[Grid, List[Elevation]]:
        lines = input.split("\n")
        
        grid = Grid(height=len(lines), width=len(lines[0]))
        
        elements: List[Elevation] = []
        
        for coordinate in grid.each_coordinate():
            character = lines[coordinate.y][coordinate.x]
            element = Elevation(height=int(character))
            grid.place_element(location=coordinate, element=element)
            elements.append(element)
            
        return grid, elements
        
