# Notes

1. regA % 8 -> regB
2. regB xor 100 -> regB
3. regA // 2^regB -> regC
4. regB xor regC -> regB
5. regB xor 100 -> regB
6. print regB % 8
7. regA // 8 -> regA
8. repeat


could maybe build backwards?

if X gives the correct digit last digit, then there should be some value between X * 8 and X * 9 that should give the second to last digit??????? That number needs to be higher than *8 because otherwise it would be truncated to 0. It also needs to be less than x*9 because that would change that number.

Doesn't seem to work. Maybe I need to try different paths?



    
    def process_while_output_matches_until_halted(self, match: List[int]):
        while not self.is_halted() and self.output_starts_with(match):
            self.process()
    
    def output_starts_with(self, match: List[int]):
        if len(self.output) < len(match):
            return False
        return ",".join(map(str,match)).startswith(",".join(self.output[:len(match)]))
    



        def find_next_digit(self, digits: List[int], digit_index: int, from_iteration: int, to_iteration: int):
        current_digit = digits[digit_index]
        
        matching_iterations = []
        
        for i in range(from_iteration, to_iteration):
            pass
            