# Create files called input.txt, test_input.txt and test_answer.txt
# If nodemon is installed, run using nodemon.cmd --exec py <path to file> -t

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


class Group:
    def __init__(self, input: str):
        self.input = input
    
    def __repr__(self):
        return self.input
    
    def get_minmax_specs_fits_from_index(self, specs: list[int], index: int):
        offset = index

        hit_chain = 0

        min = 0
        max = 0

        spec_index = 0
        while spec_index < len(specs):
            # print(f"Looking at if {specs[spec_index]} ({spec_index}) fits in {self.input[offset:]}")
            after_spec_offset = offset + specs[spec_index]
            if after_spec_offset > len(self.input): 
                # we reached the end of either the specs or the input
                # so return a slice up to the index we've reached
                return (min, spec_index)

            # keep track of hits in a row to filter out too small specs
            if self.input[offset] == "#":
                hit_chain += 1
            else:
                hit_chain = 0

            if specs[spec_index] < hit_chain:
                # this number is top small for the known hits, so go to the start
                # of the chain and backtrack in the list to see if the previous value
                # will work  
                if spec_index <= 0:
                    return (0, 0)
                spec_index -= 1
                offset -= (hit_chain  - 1)
                hit_chain = 0 # since we're not looking at the next char we need to go back one in the hit chain
                continue


            if after_spec_offset == len(self.input):
                # the last spec ends at the end of the string, so add
                # this spec and return
                if hit_chain > 0:
                    min += 1
                return (min, spec_index+1)

            if self.input[after_spec_offset] == "#":
                # the space after this spec was a # which means this group
                # doesn't fit here. Try next space.
                offset += 1
                continue
            
            if hit_chain > 0:
                min += 1
            offset += specs[spec_index] + 1
            spec_index += 1

        return (min, max)

    def get_possibilities(self, specs: list[int]):
        if len(specs) == 0:
            return 0
        return Group.get_possilities_recursive(self.input, specs, 0)

            
    def get_possilities_recursive(input: str, specs: list[int], hit_chain: int):
        # if we reached end of specs, then we should have succeeded, return 1
        if len(specs) == 0:
            return 1
        
        if len(input) == 0:
            # we still have specs but no input if there is a hit chain, check 
            # if the last spec fits, otherwise this path doesn't work
            if hit_chain == specs[0]:
                return 1

            return 0

        if input[0] == "#":
            # if we hit a #, we move forward one and increase hit chain
            return Group.get_possilities_recursive(input[1:], specs, hit_chain + 1)

        if hit_chain > 0:
            # if we have a chain, we have to check that the top of the spec
            # list is big enough
            if hit_chain > specs[0]:
                return 0
            
        # now try both and count both paths
        sum = 0
        if len(input) == specs[0]:
            sum += Group.get_possilities_recursive(input[specs[0]:], specs[1:], 0)
        if len(input) > specs[0]:
            sum += Group.get_possilities_recursive(input[specs[0] + 1:], specs[1:], 0)
        
        # try not placing a spring here
        sum += Group.get_possilities_recursive(input[1:], specs, 0)
        
        return sum


class Line:
    def __init__(self, input: str):
        [self.group_inputs, self.spec_inputs] = input.split(" ")
        
        self.specs = []
        for spec_input in self.spec_inputs.split(","):
            self.specs.append(int(spec_input))

        self.groups = []
        for group_input in self.group_inputs.split("."):
            if group_input == "":
                continue
            self.groups.append(Group(group_input))

    def __repr__(self):
        return f"{' '.join(map(lambda x: str(x), self.groups))} | {','.join(map(lambda x: str(x), self.specs))}"
    
    def solve(self):
        return solve_groups(self.groups, self.specs)

def solve_groups(groups: list[Group], specs: list[int], recursion: int = 1):
    if len(groups) == 0:
        if len(specs) != 0:
            return -1
        return 0

    for i in range(recursion):
        print(">", end="")

    print(f" {groups} | {specs}", end=" | ")
    spec_range = groups[0].get_minmax_specs_fits_from_index(specs, 0)
    
    if spec_range[1] == 0:
        print()
        return -1

        
    if spec_range[0] > spec_range[1]:
        spec_range = (spec_range[0], spec_range[0])

    print(spec_range, end=" | ")
    print(f"{specs[0:spec_range[0]]} -> {specs[0:spec_range[1]]}")

    product_sum = 0

    for spec_index in range(spec_range[0], spec_range[1] + 1):
        recursion_path = solve_groups(groups[1:], specs[spec_index:], recursion + 1)

        if recursion_path != -1:
            product_sum += recursion_path
            for i in range(recursion):
                print(">", end="")
            possibilties = groups[0].get_possibilities(specs[0:spec_index])
            for i in range(recursion):
                print(">", end="")
            print(f"=== {groups[0]} | {specs[0:spec_index]} -> {possibilties}")
            product_sum *= possibilties

    for i in range(recursion):
        print(">", end="")
    print(f"{groups[0]} {product_sum}")
    return product_sum
    


def get_result(input: str, part_b: bool = False):
    line_inputs = input.split("\n")

    sum = 0

    for line_input in line_inputs:
        line = Line(line_input)
        print(f"\n[{line}]")

        sum += line.solve()


    return sum


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
# test_result_b = get_result(test_input, True)
test_result_b = 0
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
