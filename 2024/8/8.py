from typing import Callable, Dict, List, Set, Tuple
from libraries.solution_manager import PuzzleSolution


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

class AntennaGroup:
    def __init__(self, char: str):
        self.char = char
        self.locations: List[Coordinate] = []
        self.antinode_locations: Set[Coordinate] = set()

    def __repr__(self):
        return f"[{self.char}] @ [{", ".join(map(str, self.locations))}]"

    def process_on_each_combination(
        self, callback: Callable[[Coordinate, Coordinate], any]
    ) -> Dict[Tuple[Coordinate, Coordinate], any]:

        result: Dict[Tuple[Coordinate, Coordinate], any] = {}

        for outer_i in range(len(self.locations)):
            for inner_i in range(len(self.locations)):
                if outer_i == inner_i:
                    continue

                coord_a = self.locations[outer_i]
                coord_b = self.locations[inner_i]

                callback_result = callback(coord_a, coord_b)
                result[(coord_a, coord_b)] = callback_result

        return result


class Solution(PuzzleSolution):

    def get_answer_a(self, input: str) -> int | float | str:
        height, width, antennas = self.get_elements(input)

        print(f"Width: {width}, height: {height}")

        for antenna in antennas:
            # print(antenna)
            combination_result: Dict = antenna.process_on_each_combination(
                self.get_antinode_locations
            )
            for result in combination_result.values():
                for result_component in result:
                    if self.is_location_in_map(result_component, height=height, width=width):
                        antenna.antinode_locations.add(result_component)

        # self.print_map(height, width, antennas)

        unique_antinodes = set()

        for antenna in antennas:
            for antinode_location in antenna.antinode_locations:
                unique_antinodes.add(antinode_location)
        
        # print(unique_antinodes)
        return len(unique_antinodes)

    
    def get_answer_b(self, input: str) -> int | float | str:
        height, width, antennas = self.get_elements(input)

        print(f"Width: {width}, height: {height}")

        for antenna in antennas:
            # print(antenna)
            combination_result: Dict = antenna.process_on_each_combination(
                lambda coord_a, coord_b: self.get_antinode_line(coord_a, coord_b, width, height)
            )
            for result in combination_result.values():
                for result_component in result:
                    if self.is_location_in_map(result_component, height=height, width=width):
                        antenna.antinode_locations.add(result_component)

        self.print_map(height, width, antennas)

        unique_antinodes = set()

        for antenna in antennas:
            for antinode_location in antenna.antinode_locations:
                unique_antinodes.add(antinode_location)
        
        print(unique_antinodes)
        return len(unique_antinodes)


    @staticmethod
    def is_location_in_map(
        location: Coordinate, width: int, height: int
    ) -> Tuple[Coordinate, Coordinate]:
        return location.x < width and location.x >= 0 and location.y < height and location.y >= 0

    @staticmethod
    def get_antinode_locations(
        coordinate_a: Coordinate, coordinate_b: Coordinate
    ) -> Tuple[Coordinate, Coordinate]:

        from_a_to_b = coordinate_b - coordinate_a
        from_b_to_a = coordinate_a - coordinate_b

        antinode_a = coordinate_b + from_a_to_b
        antinode_b = coordinate_a + from_b_to_a

        return (antinode_a, antinode_b)

    @staticmethod
    def get_antinode_line(
        coordinate_a: Coordinate, coordinate_b: Coordinate, width: int, height: int
    ) -> Tuple[Coordinate, Coordinate]:

        from_a_to_b = coordinate_b - coordinate_a
        from_b_to_a = coordinate_a - coordinate_b

        antinode_locations: List[Coordinate] = [coordinate_a, coordinate_b]

        current_location = coordinate_a
        direction = from_b_to_a
        iteration = 0
        while iteration < 10000:
            iteration += 1
            next_location = current_location + direction
            if not Solution.is_location_in_map(next_location, width, height):
                break
            
            antinode_locations.append(next_location)
            current_location = next_location
            
        current_location = coordinate_b
        direction = from_a_to_b
        iteration = 0
        while iteration < 10000:
            iteration += 1
            next_location = current_location + direction
            if not Solution.is_location_in_map(next_location, width, height):
                break
            
            antinode_locations.append(next_location)
            current_location = next_location
            
        return antinode_locations

    @staticmethod
    def get_elements(input: str):
        lines = input.split("\n")

        height = len(lines)
        width = len(lines[0])

        antennas: Dict[str, AntennaGroup] = {}

        for height_i in range(height):
            for width_i in range(width):
                character = lines[height_i][width_i]

                if character == ".":
                    continue

                if character in antennas:
                    antennas[character].locations.append(Coordinate(width_i, height_i))
                    continue

                new_antenna = AntennaGroup(character)
                new_antenna.locations.append(Coordinate(width_i, height_i))
                antennas[character] = new_antenna

        return height, width, antennas.values()

    @staticmethod
    def print_map(height, width, antennas):
        for height_i in range(height):
            for width_i in range(width):
                coordinate = Coordinate(width_i, height_i)
                placed = False
                
                for antenna in antennas:
                    if coordinate in antenna.antinode_locations:
                        print("#", end="", flush=True)
                        placed = True
                        break
                if placed:
                    continue
                
                for antenna in antennas:
                    if coordinate in antenna.locations:
                        print(antenna.char, end="", flush=True)
                        placed = True
                        break
                if placed:
                    continue
                

                
                print(".", end="", flush=True)
            print()
