# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

import os
from re import L
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


[input, test_input, test_answer_a, test_answer_b] = try_get_multiple_file_contents(
    "input.txt", "test_input.txt", "test_answer_a.txt", "test_answer_b.txt"
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


class PipeMap:
    def __init__(self, input):
        self.content = {}
        self.starting_position: Coordinate | None = None

        for i, line in enumerate(input.split("\n")):
            self.content[i] = {}
            for j, char in enumerate(line):
                if char == "S":
                    self.starting_position = Coordinate(i, j)

                self.content[i][j] = char

        if not self.starting_position:
            raise ValueError("Input data had no starting position")

    def draw_map(self):
        for i in range(len(self.content)):
            for j in range(len(self.content[i])):
                print(self.get_char_at_coordinate(Coordinate(i, j)), end="")
            print()

    def get_char_at_coordinate(self, coordinate: Coordinate):
        return self.content[coordinate.x][coordinate.y]

    def get_starting_position_and_starting_directions(
        self,
    ) -> tuple[Coordinate, list[Direction]]:
        directions = []
        for direction in [
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
        ]:
            if self.is_direction_possible(self.starting_position, direction):
                directions.append(direction)

        if len(directions) < 1:
            raise Exception("Could not find good direction for starting position")

        return (self.starting_position, directions)

    def is_direction_possible(self, location: Coordinate, direction: Direction):
        new_location = move(location, direction)
        char = self.get_char_at_coordinate(new_location)
        match direction:
            case Direction.UP:
                return char in "|7F"
            case Direction.RIGHT:
                return char in "-J7"
            case Direction.DOWN:
                return char in "|LJ"
            case Direction.LEFT:
                return char in "-LF"
            case _:
                raise ValueError(f"Unpexpected direction and ({direction})")

    def next_move(self, location: Coordinate, previous_direction: Direction):
        char = self.get_char_at_coordinate(location)
        match previous_direction:
            case Direction.UP:
                match char:
                    case "|":
                        return Direction.UP
                    case "7":
                        return Direction.LEFT
                    case "F":
                        return Direction.RIGHT
                    case _:
                        raise ValueError(
                            f"Direction and character mismatch ({previous_direction} | {char})"
                        )
            case Direction.RIGHT:
                match char:
                    case "-":
                        return Direction.RIGHT
                    case "J":
                        return Direction.UP
                    case "7":
                        return Direction.DOWN
                    case _:
                        raise ValueError(
                            f"Direction and character mismatch ({previous_direction} | {char})"
                        )
            case Direction.DOWN:
                match char:
                    case "|":
                        return Direction.DOWN
                    case "L":
                        return Direction.RIGHT
                    case "J":
                        return Direction.LEFT
                    case _:
                        raise ValueError(
                            f"Direction and character mismatch ({previous_direction} | {char})"
                        )
            case Direction.LEFT:
                match char:
                    case "-":
                        return Direction.LEFT
                    case "L":
                        return Direction.UP
                    case "F":
                        return Direction.DOWN
                    case _:
                        raise ValueError(
                            f"Direction and character mismatch ({previous_direction} | {char})"
                        )
            case _:
                raise ValueError(f"Unexpected direction {previous_direction}")


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


def met_at_middle(
    path_a: tuple[Coordinate, Direction],
    path_b: tuple[Coordinate, Direction],
):
    if path_a[0] == path_b[0]:
        return True

    if move(path_a[0], path_b[1]) == path_b[0]:
        return True


def get_result(input: str, part_b: bool = False):
    pipe_map = PipeMap(input)

    (
        starting_position,
        starting_directions,
    ) = pipe_map.get_starting_position_and_starting_directions()

    paths = [
        (starting_position, starting_directions[0]),
        (starting_position, starting_directions[1]),
    ]

    pipe_map.draw_map()

    steps = 0

    while steps == 0 or not met_at_middle(paths[0], paths[1]):
        steps += 1
        for i, path in enumerate(paths):
            new_position = move(path[0], path[1])
            new_direction = pipe_map.next_move(new_position, path[1])
            print(
                f"{pipe_map.get_char_at_coordinate(path[0])}{path[0]} [{get_direction_char(path[1])}] -> {pipe_map.get_char_at_coordinate(new_position)}{new_position} [{get_direction_char(new_direction)}]    ",
                end="",
            )
            paths[i] = (new_position, new_direction)
        print()

    print("MET AT MIDDLE")
    print(
        f"{pipe_map.get_char_at_coordinate(paths[0][0])}{paths[0][0]} {pipe_map.get_char_at_coordinate(paths[1][0])}{paths[1][0]}"
    )

    # next_direction = pipe_map.(current_position, current_direction)

    return steps


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
test_result_b = get_result(test_input, True)
test_b_success = check_result(test_result_b, test_answer_b)
print("---")

if test_b_success:
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
