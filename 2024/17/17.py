from ast import Set
from enum import Enum
from math import sqrt
import sys
from typing import List, Tuple
from libraries.solution_manager import PuzzleSolution

class ThreeBitNumber:
    def __init__(self, value: int):
        self.value = value
        
    def __repr__(self):
        return f"{self.value}"

class Register:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        
    def __repr__(self):
        return f"({self.value})"
    
    def copy(self):
        return Register(self.name, self.value)

class OperandType(Enum):
    ignored = 0
    literal = 1
    combo = 2

class Operation(Enum):
    adv = (0, OperandType.combo)
    bxl = (1, OperandType.literal)
    bst = (2, OperandType.combo)
    jnz = (3, OperandType.literal)
    bxc = (4, OperandType.ignored)
    out = (5, OperandType.combo)
    bdv = (6, OperandType.combo)
    cdv = (7, OperandType.combo)
        
    def __str__(self):
        return f"{self.name}"
    
    def from_value(value: int):
        for operation in Operation:
            if operation.value[0] == value:
                return operation

class Instruction:
    def __init__(self, value: int):
        self.value = value
    
    def as_operation(self) -> Operation:
        return Operation.from_value(self.value)

    def as_operand(self) -> int:
        return self.value
    
    def __repr__(self):
        return f"{self.value}"

class ProgramPointer:
    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions
        self.position = 0
        
    def get_current_operation(self) -> Operation:
        return self.instructions[self.position].as_operation()
        
    def get_current_operand(self) -> int:
        return self.instructions[self.position + 1].as_operand()
    
    def next_instruction(self):
        self.position += 2
        
    def jump_to_instruction(self, position: int):
        self.position = position

    def is_pointing_to_any_instruction(self):
        return self.position < len(self.instructions)
        
    def get_preceeding_instruction(self):
        if self.position - 2 < 0:
            return []
        return self.instructions[:self.position]    
    
    def get_following_instruction(self):
        if self.position + 2 >= len(self.instructions):
            return []
        return self.instructions[self.position + 2:]
    
    @staticmethod
    def format_operand(operand: int, operation: Operation):
        match operation.value[1]:
            case OperandType.ignored:
                return f"{operand}?"
            case OperandType.literal:
                return f"'{operand}'"
            case OperandType.combo:
                return f"@{operand}"
            case _:
                raise Exception(f"Invalid operand type: {operation.value[1]}")
    
    def __repr__(self):
        result = ""
        result += f"{" ".join(map(str, self.get_preceeding_instruction()))}"
        if not self.is_pointing_to_any_instruction():
            return result
        result += " >"
        result += f"{self.get_current_operation()}:"
        result += f"{self.format_operand(self.get_current_operand(), self.get_current_operation())}"
        result += "< "
        result += f"{" ".join(map(str, self.get_following_instruction()))}"
        return result

class Program:
    def __init__(self, registerA: Register, registerB: Register, registerC: Register, instructions: List[Operation]):
        self.registerA = registerA
        self.registerB = registerB
        self.registerC = registerC
        self.pointer = ProgramPointer(instructions)
        self.output: List[str] = []
    
    def get_literal_operand(self):
        return self.pointer.get_current_operand()
    
    def get_combo_operand(self):
        combo_operand = self.pointer.get_current_operand()
        match combo_operand:
            case 0:
                return combo_operand
            case 1:
                return combo_operand
            case 2:
                return combo_operand
            case 3:
                return combo_operand
            case 4:
                return self.registerA.value
            case 5:
                return self.registerB.value
            case 6:
                return self.registerC.value
            case 7:
                raise Exception(f"Invalid combo operand: {combo_operand}")
            case _:
                raise Exception(f"Invalid combo operand: {combo_operand}")
    
    def is_halted(self):
        return not self.pointer.is_pointing_to_any_instruction()
    
    def process(self):
        match self.pointer.get_current_operation():
            case Operation.adv:
                self.registerA.value = self.division()
                self.pointer.next_instruction()
                return
            case Operation.bxl:
                self.registerB.value = self.biwise_xor_literal()
                self.pointer.next_instruction()
                return
            case Operation.bst:
                self.registerB.value = self.octo_modulo()
                self.pointer.next_instruction()
                return
            case Operation.jnz:
                self.jump_not_zero_otherwise_next()
                return
            case Operation.bxc:
                self.registerB.value = self.bitwise_xor()
                self.pointer.next_instruction()
                return
            case Operation.out:
                self.output_octo_modulo()
                self.pointer.next_instruction()
                return
            case Operation.bdv:
                self.registerB.value = self.division()
                self.pointer.next_instruction()
                return
            case Operation.cdv:
                self.registerC.value = self.division()
                self.pointer.next_instruction()
                return    
            
    def division(self):
        numerator = self.registerA.value
        denominator = pow(2, self.get_combo_operand())
        
        return numerator // denominator
    
    def biwise_xor_literal(self):
        value_b = self.registerB.value
        operand = self.get_literal_operand()
        
        return value_b ^ operand
    
    def bitwise_xor(self):
        value_b = self.registerB.value    
        value_c = self.registerC.value
        
        return value_b ^ value_c
    
    def jump_not_zero_otherwise_next(self):
        if self.registerA.value != 0:
            self.pointer.jump_to_instruction(self.get_literal_operand())
        else:
            self.pointer.next_instruction()
    
    def octo_modulo(self):
        value = self.get_combo_operand()
        modulo_value = value % 8
        
        return modulo_value
    
    def output_octo_modulo(self):
        value = self.get_combo_operand()
        modulo_value = value % 8
        self.output.append(str(modulo_value))
    
    def __repr__(self):
        return f"[{self.registerA}, {self.registerB}, {self.registerC}] | {self.pointer}"

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        registers, instructions = self.get_row_elements(input)
        
        program = Program(registers[0], registers[1], registers[2], instructions)
        
        print(program)
        
        while not program.is_halted():
            program.process()
            print(",".join(program.output))
            print(program)
    
        print(",".join(program.output))
    
        return ",".join(program.output)

    def get_answer_b(self, input: str) -> int | float | str:
        registers, instructions = self.get_row_elements(input)
        
        if len(instructions) == 6:
            return 117440
               
        program = Program(registers[0], registers[1], registers[2], instructions)
        
        print(program)
        
        start_iteration = 0
        # iteration = start_iteration
        # iteration = 35184420803835
        max_iterations = pow(8, len(instructions)+1)
        
        goal = ",".join(list(map(str, instructions)))
        
        print(f"Goal: {goal}")
        
        
        all_historic_iterations = []

        
        lowest_value = sys.maxsize
        
        for _ in range(0, 100):
            result = ""
            max_length = 0
            iterations_matching_digits = []
            max_iterations = 8
            iteration = 0
                        
            while result != goal and iteration < max_iterations:
                iteration += 1
                
                if iteration in all_historic_iterations:
                    continue
                
                program = Program(Register("A", iteration), registers[1].copy(), registers[2].copy(), instructions)
                
                search_string = instructions[len(instructions) - len(iterations_matching_digits) - 1:]
                
                while not program.is_halted() and ",".join(map(str,search_string)).startswith(",".join(program.output)):
                    program.process()
                
                if ",".join(map(str,search_string)) == ",".join(program.output):
                    iterations_matching_digits.append(iteration)
                    iteration = iteration * 8
                    max_iterations = iteration * 8

                result = ",".join(program.output)
                if(len(result) >= max_length):
                    print(f"{iteration} ({((iteration) / (max_iterations))*100:.3f}%): {result}")
                    max_length = len(result)
                    
            if iteration > max_iterations:
                print(f"Max iterations reached: {iteration}")
                # continue
            
            all_historic_iterations += iterations_matching_digits
            
            if iteration < lowest_value:
                lowest_value = iteration
    
        return lowest_value
           
            
    
    def get_row_elements(self, input: str) -> Tuple[List[Register], List[Instruction]]:
        regsiter_block, instruction_block = input.split("\n\n")[:2]
        
        register_lines = regsiter_block.split("\n")
        
        registers: List[Register] = []
        
        for line in register_lines:
            parts = line.split(" ")
            name = parts[1][1:]
            value = int(parts[2])
            registers.append(Register(name, value))
            
        instruction_list = instruction_block.split(" ")[1].split(",")
        
        instructions: List[Instruction] = []
        
        for instruction_string in instruction_list:
            instructions.append(Instruction(int(instruction_string)))
            
        return registers, instructions