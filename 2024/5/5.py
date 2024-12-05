from typing import Dict, List, Tuple
from libraries.solution_manager import PuzzleSolution

class Node:
    def __init__(self, key):
        self.key = key
        self.verified_higher_values: Dict[int, Node] = {}
        self.verified_not_higher_values = []
        self.higher_than: List[Node] = []

    def add_higher_than(self, node):
        self.higher_than.append(node)

    def has_higher_than(self):
        return len(self.higher_than) > 0

    def find(self, value: int, exclude = []):
        # print(f"Looking for {value} in {self.key}")
        if self.key == value:
            if self.key in exclude:
                return None
            # print(f"Found {value}")
            return self
        
        if value in self.verified_not_higher_values:
            # print(f"Already verified that {value} is not higher than {self.key}")
            return None

        if not self.has_higher_than():
            # print(f"Reached end when searching for {value} in {self.key}")
            self.verified_not_higher_values.append(value)
            return None


        for node in self.higher_than:
            if value in self.verified_higher_values.keys():
                # print(f"Already verified that {value} is higher than {self.key}")
                return self.verified_higher_values[value]

            find_result = node.find(value)
            if find_result is not None:
                self.verified_higher_values[value] = find_result
                return find_result
        
        self.verified_not_higher_values.append(value)
        return None

    def __repr__(self):
        if self.has_higher_than():
            return f"{self.key} -> {self.higher_than}"
        else:
            return f"{self.key}"

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        rules, manuals = Solution.process_input(input)


        # for ordering in orderings.values():
        #     print(f"{ordering}")

        sum = 0


        for manual in manuals:
            orderings = Solution.build_rule_order(rules, manual)
            is_correct = self.check_manual(manual, orderings)
            # print(f"{is_correct} -> {manual}")
            if is_correct:
                middle_page = Solution.get_middle_page(manual)
                # print(f"Adding {middle_page}")
                sum += middle_page


        return sum

    def get_answer_b(self, input: str) -> int | float | str:
        rules, manuals = Solution.process_input(input)

        sum = 0

        for manual in manuals:
            orderings = Solution.build_rule_order(rules, manual)

            if self.check_manual(manual, orderings):
                continue

            print(f"Reordering {manual}")

            placed_pages = []

            while len(placed_pages) < len(manual):
                unplaced_pages: List[int] = []
                for page in manual:
                    if page not in placed_pages:
                        unplaced_pages.append(page)
                if len(unplaced_pages) == 0:
                    raise Exception("For some reason unplaced pages is empty")

                smallest = self.last_of_candidates(orderings, unplaced_pages)
                if smallest is None:
                    raise Exception("Something went wrong when finding smallest page")
                    
                placed_pages.append(smallest)

            placed_pages.reverse()
            print(placed_pages)

            sum += Solution.get_middle_page(placed_pages)


        return sum

    def last_of_candidates(self, orderings: Dict[int, Node], candidates: List[int]) -> Node | None:
        # print(f"Searching for smallest in {candidates}")
        
        current_candidate = candidates[0]

        while True:
            find_result = Solution.find_any_from_page(orderings, current_candidate, candidates)
            if find_result is None:
                # print(f"Smallest was {current_candidate}")
                return current_candidate
            
            current_candidate = find_result.key



    def find_any_from_page(orderings, page, candidates):
        for target_page in candidates:
            if target_page == page:
                continue

            search_result = orderings[page].find(target_page)
            if search_result is not None:
                return search_result
        return None
    
    def swap_elements_at_index(input_list, index):
        return input_list[0:index] + input_list[index + 1 : index + 2] + input_list[index : index + 1] + input_list[index + 2:]

    def get_middle_page(manual):
        if len(manual) % 2 != 1:
            raise Exception("Manual was not odd size")
        return manual[len(manual) // 2]

    def check_manual(self, manual, orderings) -> bool:
        current_node: Node | None = None

        for page in manual:
            if current_node is None:
                current_node = orderings[page]
                continue

            current_node = current_node.find(page)
            if current_node is None:
                return False

        return True
                
            

    def process_input(input: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
        lines = input.split("\n")

        rules: List[int, int] = []
        manuals: List[List[int]] = []

        is_rule_processing_done = False

        for line in lines:
            if line == "":
                is_rule_processing_done = True
                continue

            if not is_rule_processing_done:
                rule = line.split("|")
                if len(rule) != 2:
                    raise Exception("Something went wrong with input processing of rules")
                
                rule = list(map(int, rule))

                rules.append(rule)
                continue

            if is_rule_processing_done:
                manual = line.split(",")
                if len(rule) < 1:
                    raise Exception("Something went wrong with input processing of manuals")
                
                manual = list(map(int, manual))
                manuals.append(manual)
            
        
        return rules, manuals
    

    def build_rule_order(rules: List[Tuple[int, int]], manual: List[int]):
        processed_orderings: Dict[int, Node] = {}

        for rule in rules:
            rule_lower = rule[0]
            rule_higher = rule[1]

            if not (rule_lower in manual and rule_higher):
                continue

            if rule_lower in processed_orderings:
                current_ordering = processed_orderings[rule_lower]
            else:
                current_ordering = Node(rule_lower)
                processed_orderings[rule_lower] = current_ordering
            
            if rule_higher in processed_orderings:
                dependent_ordering = processed_orderings[rule_higher]
            else:
                dependent_ordering = Node(rule_higher)
                processed_orderings[rule_higher] = dependent_ordering

            current_ordering.add_higher_than(dependent_ordering)

        return processed_orderings

