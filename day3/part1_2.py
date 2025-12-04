def read_data(path: str) -> list[str]:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return data


banks = read_data("day3/input.txt")


def get_joltage(bank: str, n_batteries: int) -> int:
    bank_size = len(bank)
    first = 0
    total = ""
    for n in reversed(range(1, 1 + n_batteries)):
        # The searchable bank must
        # 1) start the index of the previous battery
        # 2) have 'size - n + 1' remaining batteries in the bank
        last = bank_size - n + 1
        searchable = bank[first:last]

        # Determine which battery should be turned on
        # and how much it contributes to the total joltage
        value = max(searchable)
        total += value

        # The first allowed index of the new searchable range
        # is 1 bigger than the index of the found battery
        first = 1 + bank.index(value, first)
    return int(total)


part_1 = 0
part_2 = 0
for bank in banks:
    part_1 += get_joltage(bank, n_batteries=2)
    part_2 += get_joltage(bank, n_batteries=12)

print(f"{part_1=}")
print(f"{part_2=}")
