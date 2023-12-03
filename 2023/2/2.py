from functools import reduce
import math


mode = ""

if mode == "test":
    test_input_file = open(file="test_input.txt", mode="r")
    test_answer_file = open(file="test_answer.txt", mode="r")
    input = test_input_file.read()
    test_answer = int(test_answer_file.read())
else:
    input_file = open(file="input.txt", mode="r")
    input = input_file.read()

game_results = input.split('\n')


product_sum = 0

for i, game_result in enumerate(game_results):
    if game_result == "":
        break
    print(".", end="", flush=True)
    if((i + 1) >= 10 and (i + 1) % 10 == 0):
        print()
    if(game_result == ""):
        break
    [game_name, game_output] = game_result.split(":")
    game_id=int(game_name.strip().split(" ")[1])
    rounds=game_output.strip().split(";")
    rounds=map(lambda text: text.strip(), rounds)
    
    min_die_amounts = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    for round in rounds:
        die_amounts = round.split(",")
        die_amounts = map(lambda text: text.strip(), die_amounts)

        for dice_amount in die_amounts:
            [number, color] = dice_amount.split(" ")
            number = int(number)
            if(number > min_die_amounts[color]):
                min_die_amounts[color] = number

    set_power = reduce(lambda amount, product: amount * product, min_die_amounts.values(), 1)
    product_sum += set_power

print()
print("Done!")

# Test
        
if mode == "test":
    if product_sum == test_answer:
        print("✅")
    else:
        print("❌")
else:
    print(product_sum)