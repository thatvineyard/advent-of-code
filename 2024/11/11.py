import inspect
from re import S
from typing import Dict, List, Tuple
from libraries.solution_manager import PuzzleSolution

class Stone:
    def __init__(self, number, amount = 1):
        self.amount = amount
        self.number = number
        
    def __repr__(self):
        return f"({self.number}x{self.amount})"
    
    def increase_amount(self, amount):
        self.amount += amount

    # RULE 1

    def is_zero(self):
        return self.number == 0

    def replace_with_1(self):
        if not self.is_zero():
            raise Exception(f"Applying {inspect.currentframe().f_code.co_name} when rule is not true")
        # print(f"replacing {self} with one")
        return Stone(1)

    # RULE 2

    def has_even_number_of_digits(self):
        return len(str(self.number)) % 2 == 0
    
    def split(self):
        if not self.has_even_number_of_digits():
            raise Exception(f"Applying {inspect.currentframe().f_code.co_name} when rule is not true")
        
        # print(f"splitting {self} into two")
        number_string = str(self.number)
        half_length = int(len(number_string) / 2) 

        return Stone(int(number_string[:half_length])), Stone(int(number_string[half_length:]))

    # RULE 3
    
    def multiply_by_2024(self):
        if self.has_even_number_of_digits() or self.is_zero():
            raise Exception(f"Applying {inspect.currentframe().f_code.co_name} when rule is not true")
        # print(f"multiplying {self} by 2024")
        return Stone(self.number * 2024)
        


class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        stone_list = self.get_row_elements(input)
        # grid, elements = self.get_grid_elements(input)
        
        
        print(stone_list)
        

        for _ in range(25):
            new_list: List[Stone] = []

            for stone in stone_list:
                if stone.is_zero():
                    new_list.append(stone.replace_with_1())
                    continue
                if stone.has_even_number_of_digits():
                    stone_a, stone_b = stone.split()
                    new_list += [stone_a, stone_b]
                    continue

                new_list.append(stone.multiply_by_2024())

            stone_list = new_list

            # print(stone_list)


        return len(stone_list)
    

    def get_answer_b(self, input: str) -> int | float | str:
        stone_list = self.get_row_elements(input)
        # grid, elements = self.get_grid_elements(input)
        
        
        print(stone_list)

        memo: Dict[int, Dict[int, List[Stone]]] = {}
        

        final_list: List[Stone] = []

        for original_stone in stone_list:
            processed_stones = self.process_stone(original_stone, 1, 75, memo)

            final_list += processed_stones

        # for memo_item in memo.items():
        #     print(f"=== {memo_item[0]} ===")
        #     for memo_iteration in memo_item[1].items():
        #         print(f"{memo_item[0]} @ {memo_iteration[0]}: {memo_iteration[1]}")

        sum = 0
        for stone in final_list:
            sum += stone.amount
        
        return sum

    def process_stone(self, current_stone: Stone, current_iteration: int, max_iterations: int, memo: Dict[int, Dict[int, List[Stone]]]):
        if current_iteration > max_iterations:
            # print(f"({current_iteration}/{max_iterations}) Reached max iterations")
            return [current_stone]
        
        current_iteration_stones = None
    
        if current_stone.number in memo:
            memoized_depths = memo[current_stone.number].keys()
            max_memoized_depth = self.max_within_limit(memoized_depths, max_iterations - current_iteration)
            if max_memoized_depth is not None:
                # print(f"({current_iteration}/{max_iterations}) Memo: {current_stone.number} @ {max_memoized_depth}: {memo[current_stone.number][max_memoized_depth]}")
                current_iteration_stones = memo[current_stone.number][max_memoized_depth]
                next_iteration = current_iteration + max_memoized_depth
                # print(f"Found memoized answer for {current_iteration} with a depth of {max_memoized_depth}, resulting in next iteraiton being {next_iteration}")

        if current_iteration_stones is None:
            current_iteration_stones = []

            if current_stone.is_zero():                        
                current_iteration_stones.append(current_stone.replace_with_1())
            elif current_stone.has_even_number_of_digits():
                stone_a, stone_b = current_stone.split()
                current_iteration_stones += [stone_a, stone_b]
            else:
                current_iteration_stones.append(current_stone.multiply_by_2024())

            # print(f"({current_iteration}/{max_iterations}) Calc: {current_stone} @ {1}: {current_iteration_stones}")
            next_iteration = current_iteration + 1

        current_iteration_stones = self.consolidate(current_iteration_stones)

        child_results = []
        for child_stone in current_iteration_stones:
            child_results += self.process_stone(child_stone, next_iteration, max_iterations, memo)
        child_results = self.consolidate(child_results)

        # print(f"({current_iteration}/{max_iterations}) Got from children: {child_results}")

        # # store in memo        
        # for previous_stone_item in child_stone_chain.items():
        #     previous_stone = previous_stone_item[1]
        #     if previous_stone.number not in memo:
        #         memo[previous_stone.number] = {}
        #     depth = current_iteration - previous_stone_item[0] + 1
        #     if depth in memo[previous_stone.number]:
        #         continue
        #     print(f"({current_stone.number}: {current_iteration}/{max_iterations}) Storing {previous_stone.number} @ {depth}: {child_results}")
        #     memo[previous_stone.number][depth] = self.consolidate(child_results)
        
        # store in memo 
        if current_stone.number not in memo:
            memo[current_stone.number] = {}
        depth = max_iterations - current_iteration + 1
        if depth not in memo[current_stone.number]:
            # print(f"({current_iteration}/{max_iterations}) Storing {current_stone.number} @ {depth}: {child_results}")
            memo[current_stone.number][depth] = child_results
        

        child_results = list(map(lambda stone: Stone(stone.number, stone.amount * current_stone.amount), child_results))
        return child_results


    def consolidate(self, stones: List[Stone]):
        consolidated_stones: List[Stone] = []


        for stone in stones:
            found_stone = None
            for existing_stone in consolidated_stones:
                if stone.number == existing_stone.number:
                    found_stone = existing_stone
                    break
            
            if found_stone is not None:
                found_stone.increase_amount(stone.amount)
            else:
                consolidated_stone = Stone(stone.number, stone.amount)
                consolidated_stones.append(consolidated_stone)
        
        return consolidated_stones

    def max_within_limit(self, search_list, limit):
        max_value = None
        for item in search_list:
            if item > limit:
                break

            if max_value is None:
                max_value = item
                continue
        
            if item > max_value:
                max_value = item
        
        return max_value


    def get_row_elements(self, input: str) -> List[Stone]:
        lines = input.split(" ")
        
        elements: List[Stone] = []
        
        for line in lines:
            elements.append(Stone(int(line)))
            
        return elements
