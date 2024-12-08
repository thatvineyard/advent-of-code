from enum import Enum
from typing import List, Tuple
from libraries.solution_manager import PuzzleSolution


class Operators(Enum):
    ADDITION = "+"
    MULTIPLICATION = "*"
    CONCATENATION = "||"

    def perform_operation(self, operand_a, operand_b):
        match self:
            case Operators.ADDITION:
                return operand_a + operand_b
            case Operators.MULTIPLICATION:
                return operand_a * operand_b
            case Operators.CONCATENATION:
                return int(str(operand_a) + str(operand_b))

class Calibration:
    
    def __init__(self, test_value: int, operands: List[int]):
        self.test_value = test_value
        self.operands = operands

    def __repr__(self):
        return f"{self.test_value}: {" ".join(map(str, self.operands))}"

    def verify(self, possible_operators: List[Operators]) -> bool:
        return self.verify_recursive(list(self.operands), possible_operators)
    
    def verify_recursive(self, operands: List[int], possible_operators: List[Operators]) -> bool:
        if len(operands) == 0:
            raise Exception("Operands list is empty. This should not happen")
        
        first = operands[0]
        
        if len(operands) == 1:
            return first == self.test_value
        
        if len(operands) > 1 and first > self.test_value:
            return False # Our operators only make the numebr bigger, so stop as soon as the number is too big
        
        
        for operator in possible_operators:
            reduction = self.reduce(operands, operator)
            child_result = self.verify_recursive(reduction, possible_operators)
            if child_result == True:
                return True
            
        return False
        
    
    @staticmethod
    def reduce(operands: List[int], operator: Operators):
        if len(operands) < 2:
            raise Exception("Too few operands")
        operand_a = operands[0]
        operand_b = operands[1]
        rest = operands[2:]
        
        result = operator.perform_operation(operand_a, operand_b)
        
        reduction = [result] + rest
        return reduction
        
        
    


class Solution(PuzzleSolution):

    def get_answer_a(self, input: str) -> int | float | str:
        calibrations = self.get_elements(input)
        
        correct_calibrations = []
        
        for calibration in calibrations:
            # print(calibration, end="", flush=True)
            if calibration.verify([Operators.ADDITION, Operators.MULTIPLICATION]) == True:
                # print("True!")
                correct_calibrations.append(calibration)
            else:
                # print()
                pass
                
        return sum(map(lambda calibration: calibration.test_value, correct_calibrations))

    def get_answer_b(self, input: str) -> int | float | str:
        calibrations = self.get_elements(input)
        
        correct_calibrations = []
        
        for calibration in calibrations:
            # print(calibration, end="", flush=True)
            if calibration.verify([Operators.ADDITION, Operators.MULTIPLICATION, Operators.CONCATENATION]) == True:
                # print("True!")
                correct_calibrations.append(calibration)
            else:
                # print()
                pass
                
        return sum(map(lambda calibration: calibration.test_value, correct_calibrations))

    @staticmethod
    def get_elements(input: str) -> List[Calibration]:
        lines = input.split("\n")
        
        elements = []
        
        for line in lines:
            test_value, operand_string = line.split(":")
            
            test_value = int(test_value)
            operands = list(map(int, filter(None, operand_string.split(" "))))
            
            elements.append(Calibration(test_value, operands))
            
        return elements
            
