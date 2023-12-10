# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import os
from re import L
from turtle import position
from typing import Callable

import aocd
import dotenv
import inquirer

dotenv.load_dotenv()

dir = os.path.dirname(__file__)


def try_get_multiple_file_contents(*filenames: list[str]):
    result = []
    for filename in filenames:
        path = os.path.join(dir, filename)
        if os.path.isfile(path):
            file = open(file=path, mode="r")
            content = file.read()
            file.close()
        else:
            content = ""
        result.append(content)
    return result


[
    input,
    test_input,
    test_answer_a,
    test_input_b,
    test_answer_b,
    test_input_b_2,
    test_answer_b_2,
] = try_get_multiple_file_contents(
    "input.txt",
    "test_input.txt",
    "test_answer_a.txt",
    "test_input_b.txt",
    "test_answer_b.txt",
    "test_input_b_2.txt",
    "test_answer_b_2.txt",
)

#####


class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"[{self.x},{self.y}]"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y

        return False


class Tile:
    def __init__(self, char: str):
        self.char = char
        self.symbol = Tile.get_symbol(char)
        self.uppiness = None

    def is_starting_tile(self):
        return self.char == "S"

    def is_ground(self):
        return self.char == "."

    def can_enter_using_direction(self, incoming_direction: Direction):
        match incoming_direction:
            case Direction.UP:
                return self.char in "|7F"
            case Direction.RIGHT:
                return self.char in "-J7"
            case Direction.DOWN:
                return self.char in "|LJ"
            case Direction.LEFT:
                return self.char in "-LF"
            case _:
                raise ValueError(f"Unpexpected direction and ({incoming_direction})")

    def set_uppiness(self, uppiness: bool):
        self.uppiness = uppiness

    def next_direction(self, incoming_direction: Direction):
        match incoming_direction:
            case Direction.UP:
                match self.char:
                    case "|":
                        return Direction.UP
                    case "7":
                        return Direction.LEFT
                    case "F":
                        return Direction.RIGHT
                    case _:
                        raise ValueError(
                            f"Direction and character mismatch ({incoming_direction}, {self})"
                        )
            case Direction.RIGHT:
                match self.char:
                    case "-":
                        return Direction.RIGHT
                    case "J":
                        return Direction.UP
                    case "7":
                        return Direction.DOWN
                    case _:
                        raise ValueError(
                            f"Direction and character mismatch ({incoming_direction}, {self})"
                        )
            case Direction.DOWN:
                match self.char:
                    case "|":
                        return Direction.DOWN
                    case "L":
                        return Direction.RIGHT
                    case "J":
                        return Direction.LEFT
                    case _:
                        raise ValueError(
                            f"Direction and character mismatch ({incoming_direction}, {self})"
                        )
            case Direction.LEFT:
                match self.char:
                    case "-":
                        return Direction.LEFT
                    case "L":
                        return Direction.UP
                    case "F":
                        return Direction.DOWN
                    case _:
                        raise ValueError(
                            f"Direction and character mismatch ({incoming_direction}, {self})"
                        )
            case _:
                raise ValueError(f"Unexpected direction {incoming_direction}")

    def get_uppiness_symbol(self):
        if self.uppiness is None:
            return " "
        if self.uppiness:
            return "▴"
        else:
            return "▾"

    def get_symbol(char: str):
        match char:
            case "|":
                return "│"
            case "-":
                return "─"
            case "7":
                return "┐"
            case "F":
                return "┌"
            case "J":
                return "┘"
            case "L":
                return "└"
            case "S":
                return "◙"
            case ".":
                return "∙"
            case _:
                raise ValueError(f"Unexpected symbol ({char})")

    def __repr__(self):
        return self.symbol


class PipeMap:
    def __init__(self, input):
        self.content: dict[int, dict[int, Tile]] = {}
        self.starting_position: Coordinate | None = None

        for i, line in enumerate(input.split("\n")):
            self.content[i] = {}
            for j, char in enumerate(line):
                tile = Tile(char)
                if tile.is_starting_tile():
                    self.starting_position = Coordinate(i, j)

                self.content[i][j] = tile

        if not self.starting_position:
            raise ValueError("Input data had no starting position")

    def draw_map(self, include_uppiness=False):
        for i in range(len(self.content)):
            for j in range(len(self.content[i])):
                if include_uppiness:
                    print_char = self.get_tile_at_coordinate(
                        Coordinate(i, j)
                    ).get_uppiness_symbol()
                else:
                    print_char = self.get_tile_at_coordinate(Coordinate(i, j))

                print(print_char, end="")
            print()

    def get_tile_at_coordinate(self, coordinate: Coordinate):
        return self.content[coordinate.x][coordinate.y]

    def set_char_at_coordinate(self, coordinate: Coordinate, char: str):
        self.content[coordinate.x][coordinate.y] = char

    def get_starting_position_and_starting_directions(
        self,
    ) -> tuple[Coordinate, Direction]:
        for direction in [
            Direction.UP,
            Direction.RIGHT,
        ]:
            if self.is_direction_possible(self.starting_position, direction):
                return (self.starting_position, direction)

        raise Exception("Could not find good direction for starting position")

    def is_direction_possible(self, location: Coordinate, direction: Direction):
        new_location = move(location, direction)
        tile = self.get_tile_at_coordinate(new_location)
        return tile.can_enter_using_direction(direction)

    def next_move(self, location: Coordinate, previous_direction: Direction):
        tile = self.get_tile_at_coordinate(location)
        return tile.next_direction(previous_direction)

    def count_row(self, row_index):
        inside = False
        row_area = 0

        previous_uppiness = None

        for tile in self.content[row_index].values():
            if tile.uppiness is None:
                if inside:
                    row_area += 1
                    print("●", end="")
                else:
                    print("◌", end="")
                continue

            print(tile.get_uppiness_symbol(), end="")
            if tile.uppiness is not None and (
                previous_uppiness is None or tile.uppiness != previous_uppiness
            ):
                inside = not inside
                previous_uppiness = tile.uppiness
        print()
        return row_area

    def count_area(self):
        sum = 0
        for i in range(len(self.content)):
            sum += self.count_row(i)
        return sum


def move(coordinate: Coordinate, direction: Direction):
    match direction:
        case Direction.UP:
            return Coordinate(coordinate.x - 1, coordinate.y)
        case Direction.RIGHT:
            return Coordinate(coordinate.x, coordinate.y + 1)
        case Direction.DOWN:
            return Coordinate(coordinate.x + 1, coordinate.y)
        case Direction.LEFT:
            return Coordinate(coordinate.x, coordinate.y - 1)


def get_direction_char(direction: Direction):
    match direction:
        case Direction.UP:
            return "↑"
        case Direction.RIGHT:
            return "→"
        case Direction.DOWN:
            return "↓"
        case Direction.LEFT:
            return "←"


def get_result(input: str, part_b: bool = False):
    pipe_map = PipeMap(input)

    (
        starting_position,
        starting_direction,
    ) = pipe_map.get_starting_position_and_starting_directions()

    current_position = starting_position
    current_direction = starting_direction

    steps = 0

    going_up = True

    while current_position != starting_position or steps == 0:
        if current_direction == Direction.UP:
            going_up = True
        if current_direction == Direction.DOWN:
            going_up = False
        pipe_map.get_tile_at_coordinate(current_position).set_uppiness(going_up)
        steps += 1
        new_position = move(current_position, current_direction)
        if new_position == starting_position:
            break
        new_direction = pipe_map.next_move(new_position, current_direction)
        current_position = new_position
        current_direction = new_direction

    pipe_map.draw_map()
    pipe_map.draw_map(True)

    # next_direction = pipe_map.(current_position, current_direction)
    if not part_b:
        return steps // 2
    else:
        return pipe_map.count_area()


#####


def check_result(result: str, answer: str):
    if answer == "":
        print("⏹ ")
    else:
        if str(result) == answer:
            print(f"🟩 {result}")
            return True
        if str(result) != answer:
            print(f"🟥 {result} (expected {answer})")
    return False


print("-- TEST A --")
test_result_a = get_result(test_input)
test_a_success = check_result(test_result_a, test_answer_a)
print("---")
print("-- TEST B --")
test_result_b = get_result(test_input_b, True)
test_b_success = check_result(test_result_b, test_answer_b)
test_result_b_2 = get_result(test_input_b_2, True)
test_b_success_2 = check_result(test_result_b_2, test_answer_b_2)
print("---")

if test_b_success or test_b_success_2:
    if inquirer.confirm("Test succeeded on one part b, run on real data?"):
        print("RUNNING PART B")
        result = get_result(input, True)

        print("RESULT PART B: ", end="")
        print(result)

        if inquirer.confirm(f"Submit result ({result})?"):
            [year, day] = os.path.dirname(__file__).split(os.path.sep)[-2:]
            aocd.submit(result, part="b", day=int(day), year=int(year))

if test_a_success:
    if inquirer.confirm("Test succeeded on one part a, run on real data?"):
        print("RUNNING PART A")
        result = get_result(input)

        print("RESULT PART A: ", end="")
        print(result)

        if inquirer.confirm(f"Submit result ({result})?"):
            [year, day] = os.path.dirname(__file__).split(os.path.sep)[-2:]
            aocd.submit(result, part="a", day=int(day), year=int(year))
