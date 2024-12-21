from ast import Set
from enum import Enum
from typing import Dict, List, Tuple
from libraries.solution_manager import PuzzleSolution

class Color(Enum):
    BLACK = "b"
    WHITE = "w"
    RED = "r"
    GREEN = "g"
    BLUE = "u"
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value


class ColorList:
    def __init__(self, colors: List[Color]):
        self.colors = colors
        
    def starts_with(self, color: Color):
        return self.colors[0] == color
    
    def __repr__(self):
        return f"{"".join(map(str,self.colors))}"
    
# class IndexedColorList(ColorList):
#     def __init__(self, colors: List[Color]):
#         self.colors = colors
#         self.index = 0
        
#     def from_color_list(color_list: ColorList):
#         return IndexedColorList(color_list.colors)
    
#     def __repr__(self):
#         result = ""
#         result += f"{''.join(map(str, self.get_preceeding_colors()))}"
#         result += f"[{self.get_current_color()}]"
#         result += f"{''.join(map(str, self.get_colors_after_index()))}"
#         return result

#     def get_preceeding_colors(self) -> List[Color]:
#         return self.colors[:self.index]

#     def get_current_color(self) -> Color:
#         return self.colors[self.index]

#     def get_colors_after_index(self) -> List[Color]:
#         return self.colors[self.index:]
    
#     def current_color_is(self, color: Color):
#         return self.colors[self.index] == color

class Towel(ColorList):
    def __init__(self, colors: List[Color]):
        if len(colors) < 1:
            raise ValueError("Towel must have at least 1 color")
        super().__init__(colors)
        

class Display(ColorList):
    def __init__(self, colors: List[Color]):
        if len(colors) < 1:
            raise ValueError("Display must have at least 1 color")
        super().__init__(colors)
        


class ColorNode:
    def __init__(self, color: Color):
        self.color = color
        self.towel: Towel | None = None
        self.children: List[ColorNode] = []

    def add_child(self, new_child):
        if not isinstance(new_child, ColorNode):
            raise ValueError("Child must be of type ColorNode")
        for child in self.children:
            if child.is_color(new_child.color):
                raise ValueError(f"Color {new_child.color} already exists in children {self.children}")
            
        self.children.append(new_child)

    def is_color(self, other_color: Color):
        return self.color == other_color
    
    def try_find(self, colors: List[Color]):
        if len(colors) < 1:
            return []
                
        if not self.is_color(colors[0]):
            return []
            
        if len(colors) == 1:
            return [self]

        longest_match_in_children = []
        for child in self.children:
            match = child.try_find(colors[1:])
            if len(match) > len(longest_match_in_children):
                longest_match_in_children = match

        return [self] + longest_match_in_children
        
    def print_full_tree(self, depth: int = 1):
        print(f"{'|' * depth}{str(self)}")
        for child in self.children:
            child.print_full_tree(depth + 1)

    def has_towel(self):
        return self.towel is not None

    def __repr__(self):
        if self.has_towel():
            return f"({self.color}:{self.towel})"
        
        return f"({self.color})"


class ColorTree:
    def __init__(self, root_color: Color):
        self.root_color = root_color
        self.root: ColorNode = ColorNode(root_color)

    def add_towel(self, towel: Towel):
        longest_path = self.root.try_find(towel.colors)
        
        if list(map(lambda x: x.color, longest_path)) == towel.colors:
            longest_path[-1].towel = towel
            # print(f"Added towel {towel} to existing path {longest_path}")
            return
        
        new_nodes = []
        current_node = longest_path[-1]
        for i in range(len(longest_path), len(towel.colors)):
            new_node = ColorNode(towel.colors[i])
            
            current_node.add_child(new_node)
            current_node = new_node
            new_nodes.append(new_node)
        
        current_node.towel = towel
        
        # print(f"Added towel {towel} to new path starting {longest_path} -> {new_nodes}")
        
    def find_all_starts_with(self, colors: List[Color]) -> List[ColorNode]:
        nodes = self.root.try_find(colors)
        if len(nodes) == 0:
            return []
        
        return list(filter(lambda node: node.has_towel(), nodes))
    
    def __repr__(self):
        return f"Tree({self.root_color})"
    
    def print_full_tree(self):
        self.root.print_full_tree()
    
    def replace_node(self, node: ColorNode, new_node: ColorNode):
        new_node.children = node.children
        

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        towel_supply, displays = self.get_row_elements(input)
        
        trees: Dict[Color, ColorTree] = {}  
        
        for color in Color:
            trees[color] = ColorTree(color)
            
        for towel in towel_supply:
            tree = trees[towel.colors[0]]
            tree.add_towel(towel)
        
        for tree in trees.values():
            print(tree)
            tree.print_full_tree()
        
        num_possible = 0
        
        for display in displays:
            print(f"Solving for display {display}... ", end="")
            start_color = display.colors[0]
            result = self.find_all_towel_combinations_in_tree(display.colors, trees)
            
            if len(result) > 0:
                print(f"{result}")
                num_possible += 1
            else:
                print("Could not solve")
            
        
        return num_possible

    def find_all_towel_combinations_in_tree(self, colors: List[Color], trees: Dict[Color, ColorTree]) -> List[Towel]:
        if len(colors) == 0:
            raise ValueError("Tried finding towel combination with empty list of colors")
        
        tree = trees[colors[0]]
        nodes_with_towels = tree.find_all_starts_with(colors)
        # print(f"Found towels {list(map(lambda node: node.towel, nodes_with_towels))} when looking for {colors} in {tree}")
        
        if len(nodes_with_towels) <= 0:
            return []
        
        for node in nodes_with_towels:
            if node.towel.colors == colors:
                return [node.towel]

            rest_of_colors = colors[len(node.towel.colors):]
            rest_result = self.find_all_towel_combinations_in_tree(rest_of_colors, trees)
            if len(rest_result) > 0:
                return [node.towel] + rest_result
            
        return []


    def get_answer_b(self, input: str) -> int | float | str:
        towel_supply, displays = self.get_row_elements(input)
        
        trees: Dict[Color, ColorTree] = {}  
        
        for color in Color:
            trees[color] = ColorTree(color)
            
        for towel in towel_supply:
            tree = trees[towel.colors[0]]
            tree.add_towel(towel)
        
        for tree in trees.values():
            print(tree)
            tree.print_full_tree()
        
        num_possible = 0
        
        memo: Dict[str, int] = {}
        
        for display in displays:
            print(f"Solving for display {display}... ", end="")
            start_color = display.colors[0]
            result = self.find_num_towel_combinations_in_tree(display.colors, trees, memo)
            
            print(f"Found {result} combinations")
            num_possible += result
            
        
        return num_possible


    def find_num_towel_combinations_in_tree(self, colors: List[Color], trees: Dict[Color, ColorTree], memo: Dict[str, int]) -> int:
        if len(colors) == 0:
            raise ValueError("Tried finding towel combination with empty list of colors")
        
        color_string = "".join(map(str, colors))
        if color_string in memo:
            print("Hit")
            return memo[color_string]
        
        tree = trees[colors[0]]
        nodes_with_towels = tree.find_all_starts_with(colors)
        # print(f"Found towels {list(map(lambda node: node.towel, nodes_with_towels))} when looking for {colors} in {tree}")
        
        if len(nodes_with_towels) <= 0:
            return 0
        
        num_combinations = 0
        
        for node in nodes_with_towels:
            if node.towel.colors == colors:
                # print("!")
                num_combinations += 1
                continue

            rest_of_colors = colors[len(node.towel.colors):]
            rest_result = self.find_num_towel_combinations_in_tree(rest_of_colors, trees, memo)
            num_combinations += rest_result
            
        memo[color_string] = num_combinations
        return num_combinations



    def get_row_elements(self, input: str) -> Tuple[List[Towel], List[Display]]:
        towel_supply_block, display_block = input.split("\n\n")
        
        towel_supplies: List[Towel] = []
        
        for towel_supply in towel_supply_block.split(", "):
            colors = list(map(lambda x: Color(x), towel_supply))
            
            towel = Towel(colors)
            towel_supplies.append(towel)
            
        displays: List[Display] = []
            
        for display in display_block.split("\n"):
            colors = list(map(lambda x: Color(x), display))
            
            display = Display(colors)
            displays.append(display)
            
        return towel_supplies, displays
        
        
