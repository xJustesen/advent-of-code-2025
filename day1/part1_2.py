MAX_POS = 100
MIN_POS = 0
DATA_FILE = "day1/input.txt"


def read_data(path: str) -> list[str]:
    with open(path, "r") as f:
        data = f.readlines()
    return data


def rotate(current: int, direction: str, steps: int) -> int:
    if direction == "L":
        new = current - steps
    elif direction == "R":
        new = current + steps
    else:
        raise ValueError(f"invalid direction: {direction}")

    # Handle rotations exceeding the max_pos
    while new >= MAX_POS:
        new = new - MAX_POS

    # Handle rortations exceeding the min_pos
    while new < MIN_POS:
        new = new + MAX_POS

    return new


# PART 1
position = 50
count = 0
instructions = read_data(DATA_FILE)
for instruction in instructions:
    direction = instruction[0]
    steps = int(instruction[1:])
    position = rotate(position, direction, steps)
    if position == 0:
        count += 1

print("PART 1", count)

# PART 2
position = 50
count = 0
for instruction in instructions:
    direction = instruction[0]
    steps = int(instruction[1:])

    for step in range(1, steps + 1):
        position = rotate(position, direction, 1)
        if position == 0:
            count += 1

print("PART 2", count)
