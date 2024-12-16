from typing import Dict, List, Set, Tuple
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
                f"Tried adding coordinate ({self}) with something that's not a coodinate ({other})"
            )

        return Coordinate(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            raise NotImplemented(
                f"Tried comparing coordinate ({self}) with something that's not a coodinate ({other})"
            )       
        
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def greater_than_or_equal_in_either_axis(self, other):
        if not isinstance(other, Coordinate):
            raise NotImplemented(
                f"Tried comparing coordinate ({self}) with something that's not a coodinate ({other})"
            )
        return self.x >= other.x or self.y >= other.y

    def scale(self, scale: int):
        return Coordinate(self.x * scale, self.y * scale)

    def zero():
        return Coordinate(0, 0)

class Button:
    def __init__(self, name: str, magnitude: Coordinate, cost: int):
        self.name = name
        self.magnitude = magnitude
        self.cost = cost
    
    def __repr__(self):
        return f"({self.name}: {self.magnitude} ({self.cost} coins))"

class Machine:
    def __init__(self, button_a: Button, button_b: Button, prize_position: Coordinate):
        self.button_a = button_a
        self.button_b = button_b
        self.prize_position = prize_position
        
    def __repr__(self):
        return f"({self.button_a}, {self.button_b}, {self.prize_position})"

    def each_button(self):
        yield self.button_a
        yield self.button_b

    def num_vectors_to_add_for_greater_or_equal_than_prize_position(self, from_position: Coordinate, vector_to_add: Coordinate):
        current_position = from_position
        num_vectors_added = 0
        iteration = 0
        while not current_position.greater_than_or_equal_in_either_axis(self.prize_position):
            if iteration > 10000:
                raise Exception("Too many iterations")
            iteration += 1


            current_position += vector_to_add
            num_vectors_added += 1
            if num_vectors_added == 100:
                return num_vectors_added
        
        return num_vectors_added

    def num_vectors_to_add_for_greater_or_equal_than_prize_position_but_smart_this_time(self, from_position: Coordinate, vector_to_add: Coordinate):
        distance = self.prize_position - from_position

        x_amount = distance.x // vector_to_add.x
        y_amount = distance.y // vector_to_add.y 

        if x_amount < y_amount:
            return x_amount
        else:
            return y_amount


class PressInstructions():
    def __init__(self):
        self.button_presses: Dict[Button, int] = {}

    def add_button_presses(self, button: Button, presses: int):
        self.button_presses[button] = presses

    def __repr__(self):
        return f"{self.button_presses}"

    def __eq__(self, other):
        if not isinstance(other, PressInstructions):
            raise NotImplemented(
                f"Tried comparing coordinate ({self}) with something that's not a coodinate ({other})"
            )       
        
        return self.button_presses == other.button_presses

    def cost(self):
        sum = 0
        for button, presses in self.button_presses.items():
            sum += button.cost * presses

        return sum
    
    def __hash__(self):
        return hash(frozenset(self.button_presses.items()))
    
class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        machines = self.get_row_elements(input)
        # grid, elements = self.get_grid_elements(input)
        
        sum = 0

        for machine in machines:
            print(f"=== {machine} ===")

            valid_instructions: Set[PressInstructions] = set()

            for button in machine.each_button():
                num_presses = machine.num_vectors_to_add_for_greater_or_equal_than_prize_position(Coordinate.zero(), button.magnitude)
                
                if num_presses is None:
                    continue

                if(button.magnitude.scale(num_presses) == machine.prize_position):
                    instruction_set = PressInstructions()
                    instruction_set.add_button_presses(button, num_presses)
                    valid_instructions.add(instruction_set)
                    break

                # print(f"{button} must be pressed at most {num_presses} times.")

                for other_button in machine.each_button():
                    revised_num_button_presses = num_presses
                    
                    if other_button == button:
                        continue

                    for i in range(num_presses + 1):
                        revised_num_button_presses = num_presses - i
                        revised_position = button.magnitude.scale(revised_num_button_presses)
                        num_other_presses = machine.num_vectors_to_add_for_greater_or_equal_than_prize_position(
                            revised_position, other_button.magnitude)
                        
                        if num_other_presses is None:
                            continue

                        if(revised_position + other_button.magnitude.scale(num_other_presses) == machine.prize_position):
                            instruction_set = PressInstructions()
                            instruction_set.add_button_presses(button, revised_num_button_presses)
                            instruction_set.add_button_presses(other_button, num_other_presses)
                            valid_instructions.add(instruction_set)
                            break

            if len(valid_instructions) == 0:
                continue
            
            cheapest_instruction = None

            for instruction in valid_instructions:
                print(f"Possible instruction was {instruction}: {instruction.cost()}")
                if cheapest_instruction is None:
                    cheapest_instruction = instruction
                    continue

                if instruction.cost() < cheapest_instruction.cost():
                    cheapest_instruction = instruction

            print(f"Cheapest instruction was {cheapest_instruction}: {cheapest_instruction.cost()}")
            sum += cheapest_instruction.cost()

        return sum

    def get_answer_b(self, input: str) -> int | float | str:
        machines = self.get_row_elements(input)
        # grid, elements = self.get_grid_elements(input)

        for machine in machines:
            machine.prize_position += Coordinate(10000000000000, 10000000000000)
        
        sum = 0

        for machine in machines:
            print(f"=== {machine} ===")

            valid_instructions: Set[PressInstructions] = set()

            for button in machine.each_button():
                num_presses = machine.num_vectors_to_add_for_greater_or_equal_than_prize_position_but_smart_this_time(Coordinate.zero(), button.magnitude)
                
                if num_presses is None:
                    continue

                if(button.magnitude.scale(num_presses) == machine.prize_position):
                    instruction_set = PressInstructions()
                    instruction_set.add_button_presses(button, num_presses)
                    valid_instructions.add(instruction_set)
                    break

                # print(f"{button} must be pressed at most {num_presses} times.")

                for other_button in machine.each_button():
                    revised_num_button_presses = num_presses
                    
                    if other_button == button:
                        continue

                    valid_instruction_for_button = self.search(machine, button, num_presses, other_button, 0, 38, 38)
                    valid_instructions |= valid_instruction_for_button

            if len(valid_instructions) == 0:
                continue
            
            cheapest_instruction = None

            for instruction in valid_instructions:
                print(f"Possible instruction was {instruction}: {instruction.cost()}")
                if cheapest_instruction is None:
                    cheapest_instruction = instruction
                    continue

                if instruction.cost() < cheapest_instruction.cost():
                    cheapest_instruction = instruction

            print(f"Cheapest instruction was {cheapest_instruction}: {cheapest_instruction.cost()}")
            sum += cheapest_instruction.cost()

        return sum

    def search(self, machine, button, num_presses, other_button, num_other_presses, exponent, original_exponent):
        if exponent < 0:
            position = button.magnitude.scale(num_presses) + other_button.magnitude.scale(num_other_presses)

            result = set()

            if(position == machine.prize_position):
                instruction_set = PressInstructions()
                instruction_set.add_button_presses(button, num_presses)
                instruction_set.add_button_presses(other_button, num_other_presses)
                result.add(instruction_set)
            
            return result
        
        valid_instructions: Set[PressInstructions] = set()
        iteration_size = int(pow(2, exponent))

        if exponent > 30:
            print(f"Searcing with iteration size: {iteration_size})")

        for i in range(2):
            revised_num_button_presses = num_presses - (i * iteration_size)
            revised_position = button.magnitude.scale(revised_num_button_presses)
            num_other_presses = machine.num_vectors_to_add_for_greater_or_equal_than_prize_position_but_smart_this_time(
                            revised_position, other_button.magnitude.scale(iteration_size))
  
            if i > iteration_size * 10:
                break

            # print(f"{num_other_presses}")


            valid_instructions |= self.search(machine, button, revised_num_button_presses, other_button, num_other_presses * iteration_size, exponent-1, original_exponent)

        return valid_instructions

    def get_row_elements(self, input: str) -> List[Machine]:
        line_groups = input.split("\n\n")
        
        machines: List[Machine] = []
        
        for line_group in line_groups:
            lines = line_group.split("\n")
            button_a_vector_parts = lines[0].split(" ")
            button_a_name = button_a_vector_parts[1][:-1]
            button_a_x = int(button_a_vector_parts[2].split("+")[1][:-1])
            button_a_y = int(button_a_vector_parts[3].split("+")[1])
            button_a = Button(button_a_name, Coordinate(button_a_x, button_a_y), 3)
            button_b_vector_parts = lines[1].split(" ")
            button_b_name = button_b_vector_parts[1][:-1]
            button_b_x = int(button_b_vector_parts[2].split("+")[1][:-1])
            button_b_y = int(button_b_vector_parts[3].split("+")[1])
            button_b = Button(button_b_name, Coordinate(button_b_x, button_b_y), 1)
            prize_parts = lines[2].split(" ")
            prize_x = int(prize_parts[1].split("=")[1][:-1])
            prize_y = int(prize_parts[2].split("=")[1])
            prize = Coordinate(prize_x, prize_y)

            machines.append(Machine(button_a, button_b, prize))
            
        return machines
    
