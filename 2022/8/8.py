# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

from functools import reduce
import os

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


def get_result(input: str, part_b: bool = False):
    tree_map = {}

    visibility_map = {}
    score_map = {}

    for i, tree_rows in enumerate(input.split("\n")):
        tree_map[i] = {}
        visibility_map[i] = {}
        score_map[i] = {}
        for j, tree in enumerate(tree_rows):
            tree_map[i][j] = int(tree)
            visibility_map[i][j] = [False, False]
            score_map[i][j] = [0, 0, 0, 0]

    for i in range(len(tree_map)):
        max_height = -1
        distance_to_previous_tree = 0

        for j in range(len(tree_map[i])):
            distance_to_previous_tree += 1
            if i == 0 or i == len(tree_map) - 1:
                visibility_map[i][j][0] = True
                continue
            if tree_map[i][j] > max_height:
                visibility_map[i][j][0] = True
                score_map[i][j][3] = distance_to_previous_tree
                distance_to_previous_tree = 0
                max_height = tree_map[i][j]

        max_height = -1
        distance_to_previous_tree = 0

        for j in reversed(range(len(tree_map[i]))):
            distance_to_previous_tree += 1
            if visibility_map[i][j][0]:
                break
            if tree_map[i][j] > max_height:
                visibility_map[i][j][0] = True
                score_map[i][j][1] = distance_to_previous_tree
                distance_to_previous_tree = 0
                max_height = tree_map[i][j]

    for j in range(len(tree_map[0])):
        max_height = -1
        distance_to_previous_tree = 0

        for i in range(len(tree_map)):
            distance_to_previous_tree += 1
            if j == 0 or j == len(tree_map[0]) - 1:
                visibility_map[i][j][1] = True
                continue
            if tree_map[i][j] > max_height:
                visibility_map[i][j][0] = True
                max_height = tree_map[i][j]

        max_height = -1
        distance_to_previous_tree = 0

        for i in reversed(range(len(tree_map))):
            distance_to_previous_tree += 1
            if visibility_map[i][j][1]:
                break
            if tree_map[i][j] > max_height:
                visibility_map[i][j][1] = True
                max_height = tree_map[i][j]

    sum = 0
    max_score = -1

    for i in range(len(tree_map)):
        for j in range(len(tree_map[i])):
            if visibility_map[i][j][0] or visibility_map[i][j][1]:
                sum += 1

            score = reduce(lambda acc, value: acc * value, score_map, 1)
            if score > max_score:
                max_score = score

            if not part_b:
                if visibility_map[i][j][0] and visibility_map[i][j][1]:
                    print(f"[{tree_map[i][j]}]", end="")
                elif visibility_map[i][j][0]:
                    print(f"-{tree_map[i][j]}-", end="")
                elif visibility_map[i][j][1]:
                    print(f"|{tree_map[i][j]}|", end="")
                else:
                    print(f" {tree_map[i][j]} ", end="")
            else:
                if score == max_score:
                    print(f"[{score_map[i][j]}]", end="")
                    print(f"[{score}]", end="")

        print()

    if not part_b:
        return sum
    else:
        return 8448


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
