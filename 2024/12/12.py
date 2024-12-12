from typing import Dict, List, Tuple
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
                f"Tried to perform subtraction on coordinate ({self}) with something that's not a coodinate ({other})"
            )

        return Coordinate(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    def __eq__(self, value):
        if not isinstance(value, Coordinate):
            raise NotImplemented(
                f"Tried to perform equals check on coordinate ({self}) with something that's not a coodinate ({other})"
            )
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return self.__repr__().__hash__()

    def each_surrounding_coordinate(self):
        yield Coordinate(self.x + 0, self.y + 1)
        yield Coordinate(self.x + 1, self.y + 0)
        yield Coordinate(self.x + 0, self.y - 1)
        yield Coordinate(self.x - 1, self.y + 0)

    def is_neighbor(self, other):
        if not isinstance(other, Coordinate):
            raise NotImplemented(
                f"Tried checking if coordinate ({self}) was a neighbor with something that's not a coodinate ({other})"
            )
        
        if other.x == self.x and abs(other.y - self.y) == 1:  
            return True
        if other.y == self.y and abs(other.x - self.x) == 1:  
            return True
        
        return False

class Plot:
    def __init__(self, character):
        self.character = character
        self.locations: List[Coordinate] = []
        
    def __repr__(self):
        return f"({self.character}[{self.count_area()}])"
            
    def each_location(self):
        for coordinate in self.locations:
            yield coordinate

    def add_location(self, location: Coordinate):
        self.locations.append(location)

    def count_area(self):
        return len(self.locations)
    
    def split_to_contiguous_plots(self):
        contiguous_plots: List[Plot] = []

        for location in self.locations:
            neighbor_plots: List[Plot] = []
            for contiguous_plot in contiguous_plots:
                for contiguous_plot_location in contiguous_plot.locations:
                    if location.is_neighbor(contiguous_plot_location):
                        neighbor_plots.append(contiguous_plot)
                        break
                    
            if len(neighbor_plots) == 0: 
                new_contiguous_plot = Plot(self.character)
                new_contiguous_plot.add_location(location)
                contiguous_plots.append(new_contiguous_plot)
                continue

            if len(neighbor_plots) == 1:
                neighbor_plot = neighbor_plots[0]

                neighbor_plot.add_location(location)

            if len(neighbor_plots) > 1:
                combined_plot = None

                for neighbor_plot in neighbor_plots:
                    if combined_plot is None:
                        combined_plot = neighbor_plot
                        continue

                    for neighbor_location in neighbor_plot.locations:
                        combined_plot.add_location(neighbor_location)

                    contiguous_plots.remove(neighbor_plot)

                combined_plot.add_location(location)
        
        return contiguous_plots

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.plot_ownership: Dict[Coordinate, Plot] = {}
    
    def assign_location_to_plot(self, location: Coordinate, plot: Plot):
        self.plot_ownership[location] = plot

    def is_in_bounds(self, coordinate: Coordinate) -> bool:
        return coordinate.x < self.width and coordinate.x >= 0 and coordinate.y < self.height and coordinate.y >= 0
    
    def each_coordinate(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Coordinate(x, y)
    
    def try_get_plot(self, location: Coordinate) -> Plot:
        if location in self.plot_ownership:
            return self.plot_ownership[location]
        else:
            return None
    
    def get_neighbors(self, location: Coordinate) -> List[Plot]:
        result = []
        for surrounding_coordinate in location.each_surrounding_coordinate():
            plot = self.try_get_plot(surrounding_coordinate)
            result.append(plot)
        
        return result

    def get_neighbors_and_coordinates(self, location: Coordinate) -> List[Tuple[Plot, Coordinate]]:
        result = []
        for surrounding_coordinate in location.each_surrounding_coordinate():
            plot = self.try_get_plot(surrounding_coordinate)
            result.append((plot, surrounding_coordinate))
        
        return result
    
class Border:
    def __init__(self, inside_location: Coordinate, outside_location: Coordinate):
        self.inside_location = inside_location
        self.outside_location = outside_location

    def is_neighbor(self, other):
        if not isinstance(other, Border):
            raise NotImplementedError(
                f"Tried checking if border ({self}) was a neighbor with something that's not a border ({other})"
            )
        
        return self.inside_location.is_neighbor(other.inside_location) and self.outside_location.is_neighbor(other.outside_location)
    
class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        grid, plots = self.get_grid_elements(input)
        
        result = 0

        for plot in plots:
            # print(f"==={plot}===")

            plot_cost = 0

            contiguous_plots = plot.split_to_contiguous_plots()

            for contiguous_plot in contiguous_plots:

                border_length = 0

                for plot_location in contiguous_plot.each_location():
                    plot_location_border_length = 0
                    for neighbor_plot in grid.get_neighbors(plot_location):
                        if neighbor_plot != plot:
                            plot_location_border_length += 1

                    # print(f"{plot_location}: {plot_location_border_length}")
                    border_length += plot_location_border_length
            
                plot_cost += border_length * contiguous_plot.count_area()
            

            result += plot_cost
            # print(f"---{plot}: {plot_cost}")

        return result

    def get_answer_b(self, input: str) -> int | float | str:
        grid, plots = self.get_grid_elements(input)
        
        result = 0

        for plot in plots:
            # print(f"==={plot}===")

            plot_cost = 0

            contiguous_plots = plot.split_to_contiguous_plots()

            for contiguous_plot in contiguous_plots:

                borders = []


                for plot_location in contiguous_plot.each_location():
                    for neighbor_plot_and_coordinates in grid.get_neighbors_and_coordinates(plot_location):
                        if neighbor_plot_and_coordinates[0] != plot:
                            borders.append(Border(plot_location, neighbor_plot_and_coordinates[1]))

                
            
                plot_cost += len(self.split_into_contiguous_borders(borders)) * contiguous_plot.count_area()
            

            result += plot_cost
            # print(f"---{plot}: {plot_cost}")

        return result
    
    @staticmethod
    def split_into_contiguous_borders(borders: List[Border]):
        contiguous_borders: List[List[Border]] = []

        for border in borders:
            neighbor_borders: List[List[Border]] = []
            for contiguous_border in contiguous_borders:
                for contiguous_border_part in contiguous_border:
                    if border.is_neighbor(contiguous_border_part):
                        neighbor_borders.append(contiguous_border)
                        break
                    
            if len(neighbor_borders) == 0: 
                contiguous_borders.append([border])
                continue

            if len(neighbor_borders) == 1:
                neighbor_borders[0].append(border)

            if len(neighbor_borders) > 1:
                combined_border = None

                for neighbor_border in neighbor_borders:
                    if combined_border is None:
                        combined_border = neighbor_border
                        continue

                    for neighbor_border_part in neighbor_border:
                        combined_border.append(neighbor_border_part)

                    contiguous_borders.remove(neighbor_border)

                combined_border.append(border)
        
        return contiguous_borders



    def get_row_elements(self, input: str) -> List[Plot]:
        lines = input.split("\n")
        
        elements: List[Plot] = []
        
        for line in lines:
            elements.append(Plot(line[0]))
            
        return elements
        
    @staticmethod
    def get_grid_elements(input: str) -> Tuple[Grid, List[Plot]]:
        lines = input.split("\n")
        
        grid = Grid(height=len(lines), width=len(lines[0]))
        
        elements: List[Plot] = []
        
        for coordinate in grid.each_coordinate():
            character = lines[coordinate.y][coordinate.x]
            found_existing_plot = None
            for existing_plot in elements:
                if existing_plot.character == character:
                    found_existing_plot = existing_plot
                    break
            if found_existing_plot is None:
                plot = Plot(character=character)
                elements.append(plot)
            else:
                plot = found_existing_plot

            plot.add_location(coordinate)
            grid.assign_location_to_plot(coordinate, plot)

            
        return grid, elements
        
