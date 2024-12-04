import os
import traceback
from types import TracebackType
from typing import Tuple

import aocd
import inquirer
from libraries import file_manager
from libraries.solution_manager import SolutionManager
from libraries.watcher import Watcher
from libraries import cli

SOLUTION_CLASS_NAME="Solution"
INPUT_FILE_NAME="input.txt"
INPUT_B_FILE_NAME="input_b.txt"
TEST_INPUT_FILE_NAME="test_input.txt"
TEST_INPUT_B_FILE_NAME="test_input_b.txt"
TEST_ANSWER_A_FILE_NAME="test_answer_a.txt"
TEST_ANSWER_B_FILE_NAME="test_answer_b.txt"

watch_date = cli.get_date()

class Runner:
  
    def __init__(self, watch_date: Tuple[int, int, int]):
        self.solution_dir = file_manager.get_date_dir(watch_date)
        self.solution_path = os.path.join(self.solution_dir, f"{watch_date[2]}.py")
        self.solution_manager = SolutionManager(solution_path=self.solution_path, class_name=SOLUTION_CLASS_NAME)
        self.watcher = Watcher(self.solution_dir, self.on_change)
        self.puzzle = aocd.models.Puzzle(watch_date[0], watch_date[2])

    def on_change(self):
        self.solution_manager.load_solution()

        print("============")
        print("🧪 TEST A   ")
        print("------------")

        if self.check_solved("a"):
            print("Already solved!")
        else:

            test_input_a = self.try_get_file_contents(TEST_INPUT_FILE_NAME)
            test_answer_a = self.try_get_file_contents(TEST_ANSWER_A_FILE_NAME)

            try:
                test_solution_a = self.solution_manager.run_solution_a(test_input_a)
                print("------------")
                test_a_success = Runner.check_result(test_solution_a, test_answer_a)

                if test_a_success:
                    if inquirer.confirm("Test succeeded on one part a, run on real data?"):
                        print("------------")
                        input_a = self.try_get_file_contents(INPUT_FILE_NAME)
                        result = self.solution_manager.run_solution_a(input_a)

                        print("RESULT PART A: ", end="")
                        print(result)

                        if inquirer.confirm(f"Submit result ({result})?"):
                            aocd.submit(result, part="a", year=watch_date[0], day=watch_date[2])
                            self.puzzle = aocd.models.Puzzle(year=watch_date[0], day=watch_date[2])
                            if self.check_solved("a"):
                                print("Success!")

            except Exception as e:
                traceback.print_exc()
                print(f"⚠️  Running failed because of exception: {e}")
        
        print("============")
        print("")
        print("============")
        print("🧪 TEST B   ")
        print("------------")

        if self.check_solved("b"):
            print("Already solved!")
        else:
            test_input_b = self.try_get_file_contents(TEST_INPUT_B_FILE_NAME)
            if test_input_b is None:
                test_input_b = self.try_get_file_contents(TEST_INPUT_FILE_NAME)
            test_answer_a = self.try_get_file_contents(TEST_ANSWER_B_FILE_NAME)

            try:
                test_solution_b = self.solution_manager.run_solution_b(test_input_b)
                print("------------")
                print("Result: ")
                test_b_success = Runner.check_result(test_solution_b, test_answer_a)

                if test_b_success:
                    if inquirer.confirm("Test succeeded on one part a, run on real data?"):
                        print("------------")
                        input_b = self.try_get_file_contents(INPUT_B_FILE_NAME)
                        if input_b is None:
                            input_b = self.try_get_file_contents(INPUT_FILE_NAME)
                        result = self.solution_manager.run_solution_b(input_b)

                        print("RESULT PART B: ", end="")
                        print(result)

                        if inquirer.confirm(f"Submit result ({result})?"):
                            aocd.submit(result, part="b", year=watch_date[0], day=watch_date[2])
                            self.puzzle = aocd.models.Puzzle(year=watch_date[0], day=watch_date[2])
                            if self.check_solved("b"):
                                print("Success!")


            except Exception as e:
                traceback.print_exc()
                print(f"⚠️  Running failed because of exception: {e}")
            
        print("============")

    def check_solved(self, part: str):
        try:
            if part == "a":
                self.puzzle.answer_a
                return True
            if part == "b":
                self.puzzle.answer_b
                return True
        except AttributeError:
            return False

    def check_result(result: str, answer: str):
        if result is None or result == "":
            print("⚠️  No result provided")
            return False
        
        if answer is None or answer == "":
            print(f"⬜ {result} (no answer provided)")
            return False
        else:
            if str(result) == answer:
                print(f"🟩 {result}")
                return True
            if str(result) != answer:
                print(f"🟥 {result} (expected {answer})")
        return False

    def try_get_file_contents(self, filename: str):
        path = os.path.join(self.solution_dir, filename)

        if not os.path.isfile(path):
            return None
        
        file = open(file=path, mode="r")
        content = file.read()
        file.close()
        return content

    def start(self):
        self.watcher.start()


runner = Runner(watch_date)
runner.start()