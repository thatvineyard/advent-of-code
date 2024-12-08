import math
from typing import List, Tuple
from libraries.solution_manager import PuzzleSolution

class Reading:
    def __init__(self, bits: List[int]):
        self.bits = bits
        
    def __repr__(self):
        return f"[{self.bits}]"
    
    def __add__(self, other):
        return Reading(list(map(sum, zip(self.bits, other.bits))))
    
    def __sub__(self, other):
        return Reading(list(map(sum, zip(self.bits, map(lambda x: -x, other.bits)))))
    
    def __mul__(self, other):
        return Reading(list(map(lambda x, y: x * y, zip(self.bits, map(lambda x: -x, other.bits)))))
        
    def scale(self, scale):
        return Reading(list(map(lambda x: x* scale, self.bits)))

    def normalize(self):
        bits = []
        for bit in self.bits:
            if bit > 0:
                bits.append(1)
            else:
                bits.append(0)
                
        return Reading(bits)
    
    def invert(self):
        bits = []
        for bit in self.bits:
            if bit == 0:
                bits.append(1)
            else:
                bits.append(0)
                
        return Reading(bits)
        
    
    def to_decimal(self):
        
        position = 0
        
        reversed_bits = list(self.bits)
        reversed_bits.reverse()

        result = 0

        for bit in reversed_bits:
            if bit == 1:
                result += int(math.pow(2, position))
            position += 1
        
        return result
    
    def size(self):
        return len(self.bits)

    @staticmethod
    def identity(size):
        return Reading([1 for _ in range(size)])

    @staticmethod
    def zero(size):
        return Reading([0 for _ in range(size)])

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        readings = self.get_row_elements(input)
        
        size = readings[0].size()
        
        result = Reading.zero(size)
        
        for reading in readings:
            result += reading.scale(2) - Reading.identity(size)
        
        return result.normalize().to_decimal() * result.normalize().invert().to_decimal()
        

    def get_answer_b(self, input: str) -> int | float | str:
        return ""

    def get_row_elements(self, input: str) -> List[Reading]:
        lines = input.split("\n")
        
        elements: List[Reading] = []
        
        for line in lines:
            elements.append(Reading(list(map(int, line))))
            
        return elements

