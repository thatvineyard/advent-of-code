import aocd


def is_solved(year: int, day: int, part: str = "a"):
    puzzle = aocd.models.Puzzle(year=year, day=day)
    if part == "a":
        return puzzle.answer_a is not None
    if part == "b":
        return puzzle.answer_b is not None

