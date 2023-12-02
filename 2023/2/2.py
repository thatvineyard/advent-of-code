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

max_die_amonuts = {
    "red": 12,
    "green": 13,
    "blue": 14
}

id_sum = 0

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
    
    game_failed = False

    for round in rounds:
        die_amounts = round.split(",")
        die_amounts = map(lambda text: text.strip(), die_amounts)

        for dice_amount in die_amounts:
            [number, color] = dice_amount.split(" ")
            number = int(number)
            if(number > max_die_amonuts[color]):
                game_failed = True
        
    if not game_failed:
        id_sum += game_id

print()
print("Done!")

# Test
        
if mode == "test":
    if id_sum == test_answer:
        print("✅")
    else:
        print("❌")
else:
    print(id_sum)