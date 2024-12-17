import os
import time
from turtle import pos
from typing import List, Tuple
from PIL import Image
from libraries.solution_manager import PuzzleSolution

def load_mask_image_to_matrix(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        width, height = img.size

        pixel_matrix = []
        for y_i in range(height):
            row = []
            for x_i in range(width):
                pixel = img.getpixel((x_i, y_i))
                row.append(pixel[0] > 200)
            pixel_matrix.append(row)

    return pixel_matrix

class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented(
                f"Tried adding coordinate ({self}) with something that's not a coodinate ({other})"
            )

        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented(
                f"Tried to perform subtraction on coordinate ({self}) with something that's not a coodinate ({other})"
            )

        return Vector(self.x - other.x, self.y - other.y)

    def scale(self, scale: int):
        return Vector(self.x * scale, self.y * scale)
    
    def __repr__(self):
        return f"{self.x},{self.y}"

    def __eq__(self, value):
        if not isinstance(value, Vector):
            raise NotImplemented(
                f"Tried to perform equals check on coordinate ({self}) with something that's not a coodinate ({value})"
            )
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return self.__repr__().__hash__()

    def zero():
        return Vector(0, 0)
    
    def one():
        return Vector(1, 1)

class Robot:
    def __init__(self, position: Vector, velocity: Vector):
        self.position = position
        self.velocity = velocity
        
    def __repr__(self):
        return f"(p={self.position} v={self.velocity}]"

    
class Grid:
    def __init__(self, width, height, origin = Vector(0,0)):
        self.width = width
        self.height = height
        self.origin = origin

    def __repr__(self):
        return f"({self.width}x{self.height}@{self.origin})"
    
    def __hash__(self):
        return hash(self.width) + hash(self.height) + hash(self.origin)

    def is_in_bounds(self, coordinate: Vector) -> bool:
        relative_coordinate = coordinate - self.origin
        return relative_coordinate.x < self.width and relative_coordinate.x >= 0 and relative_coordinate.y < self.height and relative_coordinate.y >= 0
    
    def each_coordinate(width, height):
        for y in range(height):
            for x in range(width):
                yield Vector(x, y)

    def calculate_wrapped_position(self, position: Vector, coordinate: Vector, iterations: int):
        new_position = position + coordinate.scale(iterations)
        new_position.x = new_position.x % self.width
        new_position.y = new_position.y % self.height
        return new_position

    def count_robots_in_quadrants(self, num_quadrants_x: int, num_quadrants_y: int, robots: List[Robot]):
        
        quadrant_counts = {}
        
        for y_i in range(num_quadrants_y):
            quadrant_counts[y_i] = {}
            for x_i in range(num_quadrants_x):
                quadrant = Grid(self.width // num_quadrants_x, self.height // num_quadrants_y, Vector((((self.width + 1) * x_i) // num_quadrants_x), (((self.height + 1) * y_i) // num_quadrants_y)))
                quadrant_counts[y_i][x_i] = 0
                            
                for robot in robots:
                    if quadrant.is_in_bounds(robot.position):
                        quadrant_counts[y_i][x_i] += 1

        return quadrant_counts

    def print_with_robots(self, robots: List[Robot]):
        for height_i in range(self.height):
            for width_i in range(self.width):
                robot_found = False
                for robot in robots:
                    if robot.position == Vector(width_i, height_i):
                        robot_found = True
                        break
                if robot_found:
                    print("X", end="")
                else:
                    print(".", end="")
            print()

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        grid, robots = self.get_row_elements(input)

        for robot in robots:
            robot.position = grid.calculate_wrapped_position(robot.position, robot.velocity, 100)

        quadrant_counts = grid.count_robots_in_quadrants(2, 2, robots)
        product = 1

        for y_i in range(len(quadrant_counts)):
            for x_i in range(len(quadrant_counts[y_i])):
                product = product * quadrant_counts[y_i][x_i]
                
        return product

    def get_answer_b(self, solution_input: str) -> int | float | str:
        grid, robots = self.get_row_elements(solution_input)
        
        num_robots = len(robots)
        
        image_file_name = "mask.png"
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_file_name)
        mask_matrix = load_mask_image_to_matrix(image_path)
        mask_height = len(mask_matrix)
        mask_width = len(mask_matrix[0])
        
        for y_i in range(mask_height):
            for x_i in range(mask_width):
                if mask_matrix[y_i][x_i]:
                    print("▮  ", end="")
                else:
                    print("▯  ", end="")
                    
            print()
        
        print()
        
        
        concentration_threshold = 0.1
        positive_match_score = 1
        negative_match_score = 1
        highest_score = 0
        high_match_iterations = []        
        
        for i in range(0, 10000):
        # for i in range(7700, 7800):
            if i % 100 == 0:
                print(i)
            moved_robots = []
            
            for robot in robots:
                moved_robot = Robot(robot.position, robot.velocity)
                moved_robot.position = grid.calculate_wrapped_position(moved_robot.position, moved_robot.velocity, i)
                moved_robots.append(moved_robot)
                    
            quadrant_counts = grid.count_robots_in_quadrants(mask_width, mask_height, moved_robots)

            max_count = 0
            for y_i in range(len(quadrant_counts)):
                for x_i in range(len(quadrant_counts[y_i])):
                    count = quadrant_counts[y_i][x_i]
                    if count > max_count:
                        max_count = count

            score = 0

            for y_i in range(len(quadrant_counts)):
                for x_i in range(len(quadrant_counts[y_i])):
                    count = quadrant_counts[y_i][x_i]
                    concentration = count / max_count
                    
                    pixel_is_active =  concentration > concentration_threshold
                    mask_pixel_is_active = mask_matrix[y_i][x_i]
                    
                    if pixel_is_active and mask_pixel_is_active:
                        score += positive_match_score
                    if not pixel_is_active and not mask_pixel_is_active:
                        score += negative_match_score
                    
            if score <= highest_score:
                continue
            
            highest_score = score
            high_match_iterations.append(i)
            
            print(f"Iteration {i} - Score: {score}")
            for y_i in range(len(quadrant_counts)):
                for x_i in range(len(quadrant_counts[y_i])):
                    count = quadrant_counts[y_i][x_i]
                    concentration = count / max_count
                    pixel_is_active =  concentration > concentration_threshold
                    
                    if pixel_is_active:    
                        print("▮  ", end="")
                    else:
                        print("▯  ", end="")           
                print()

        for iteration in high_match_iterations:
            moved_robots = []
            
            for robot in robots:
                moved_robot = Robot(robot.position, robot.velocity)
                moved_robot.position = grid.calculate_wrapped_position(moved_robot.position, moved_robot.velocity, iteration)
                moved_robots.append(moved_robot)

            print("---------------------------")
            print(f"Iteration {iteration}")
            grid.print_with_robots(moved_robots)
            print("---------------------------")
            print()

    def get_row_elements(self, input: str) -> Tuple[Grid, List[Robot]]:
        lines = input.split("\n")
        
        if len(lines) < 15:
            grid = Grid(11, 7)
        else:
            grid = Grid(101, 103)

        robots: List[Robot] = []
        
        for line in lines:
            line_parts = line.split(" ")
            position_parts = line_parts[0].split("=")[1].split(",")
            position = Vector(int(position_parts[0]), int(position_parts[1]))
            velocity_parts = line_parts[1].split("=")[1].split(",")
            velocity = Vector(int(velocity_parts[0]), int(velocity_parts[1]))
            robots.append(Robot(position, velocity))
            
        return grid, robots
