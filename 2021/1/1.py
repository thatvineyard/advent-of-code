import time
from libraries.solution_manager import PuzzleSolution

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        readings = input.split("\n")
        readings = list(map(int, readings))

        sum = 0

        for index in range(len(readings) - 1):
            if readings[index] - readings[index + 1] < 0:
                sum += 1

        return sum

    def get_answer_b(self, input: str) -> int | float | str:
        readings = input.split("\n")
        readings = list(map(int, readings))

        sum = 0

        previous_average = None

        for index in range(len(readings) - 2):            
            current_average = readings[index] + readings[index + 1] + readings[index + 2]
            
            if previous_average is None:
                previous_average = current_average
                continue

            if current_average > previous_average:
                sum += 1

            previous_average = current_average

        return sum
