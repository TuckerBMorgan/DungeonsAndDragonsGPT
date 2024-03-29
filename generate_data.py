import random
import json
import os
import subprocess

data_file = "data.json"
character_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Kevin", "Laura", "Mallory", "Nancy", "Oscar", "Peggy", "Quentin", "Romeo", "Sybil", "Trent", "Ursula", "Victor", "Walter", "Xander", "Yvonne", "Zelda"]

# https://stackoverflow.com/a/25802742/3696113
def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
def read_from_clipboard():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

while True:
    num_characters = random.randint(2, 10)
    teams = None
    while True:
        teams = [random.randint(0, 1) for j in range(num_characters)]
        has_0 = False
        has_1 = False
        for j in range(num_characters):
            if teams[j] == 0:
                has_0 = True
            elif teams[j] == 1:
                has_1 = True
        if has_0 and has_1:
            break
    my_index = random.randint(0, num_characters - 1)
    board_size = random.randint(4, 8)

    board = [[None for k in range(board_size)] for j in range(board_size)]
    positions = []
    for j in range(num_characters):
        unoccupied_position = None
        while True:
            unoccupied_position = (random.randint(0, board_size - 1), random.randint(0, board_size - 1))
            if board[unoccupied_position[0]][unoccupied_position[1]] == None:
                break
        board[unoccupied_position[0]][unoccupied_position[1]] = j
        positions.append(unoccupied_position)

    board_str = ""
    for k in range(board_size):
        for j in range(board_size):
            if board[j][k] == None:
                board_str += "-"
            else:
                board_str += character_names[board[j][k]][0]
        board_str += "\n"

    teammates = "".join([f"{character_names[j]} (health: {random.randint(1, 10)}, damage: {random.randint(1, 3)})\n" for j in range(num_characters) if teams[j] == teams[my_index]])
    enemies = "".join([f"{character_names[j]} (health: {random.randint(1, 10)}, damage: {random.randint(1, 3)})\n" for j in range(num_characters) if teams[j] != teams[my_index]])

    actions = []
    for j in range(positions[my_index][0] - 1, positions[my_index][0] + 2):
        if j < 0 or j >= board_size:
            continue
        for k in range(positions[my_index][1] - 1, positions[my_index][1] + 2):
            if k < 0 or k >= board_size:
                continue
            if board[j][k] == None or (j == positions[my_index][0] and k == positions[my_index][1]):
                actions.append(("M", (j, k)))
            elif teams[board[j][k]] != teams[my_index]:
                actions.append(("A", (j, k)))

    moves = "".join([f"{j} : I can move to {actions[j][1]}\n" for j in range(len(actions)) if actions[j][0] == "M"])
    if len(moves) == 0:
        moves = "None\n"
    attacks = "".join([f"{j} : I can attack {character_names[board[actions[j][1][0]][actions[j][1][1]]]} at {actions[j][1]}\n" for j in range(len(actions)) if actions[j][0] == "A"])
    if len(attacks) == 0:
        attacks = "None\n"
    actions_str = "".join([f"{j} : I can move to {actions[j][1]}\n" if actions[j][0] == "M" else f"{j} : I can attack {character_names[board[actions[j][1][0]][actions[j][1][1]]]} at {actions[j][1]}\n" for j in range(len(actions))])

    turn_order = [character_names[j] for j in range(num_characters) if j != my_index]
    random.shuffle(turn_order)
    turn_order = [character_names[my_index]] + turn_order
    turn_order_str = "\n".join(turn_order)

    # print(f"num_characters {num_characters}")
    # print(f"teams {teams}")
    # print(f"my_index {my_index}")
    # print(f"board_size {board_size}")
    # print(f"positions {positions}")
    # print()

    prompt = f"""I am {character_names[my_index]} represented by the letter {character_names[my_index][0]}
I have {random.randint(1, 10)} health
I can do {random.randint(1, 3)} damage per turn
I can move 1 tile per turn
My attack range is 1 tile
I am at position {positions[my_index]}

My teammates are:
{teammates}
My enemies are:
{enemies}
My valid moves are:
{moves}
My valid attacks are:
{attacks}
The board looks like:
{board_str}
The turn order is:
{turn_order_str}

Choose an action:
{actions_str}"""

    write_to_clipboard(prompt)
    print("Copied to clipboard")

    input("Press enter to continue")
    response = read_from_clipboard()

    if not os.path.exists(data_file):
        data = {"data": []}
    else:
        with open(data_file, 'r') as file:
            data = json.load(file)

    data["data"].append({prompt: response})
    print("Data has " + str(len(data["data"])) + " rows")

    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)