DATA_FILE = "day2/input.txt"


def read_data(path: str) -> list[str]:
    with open(path, "r") as f:
        data = f.readlines()
    return data[0].split(",")


def count_duplicates(id_: str) -> dict[str, int]:
    """Return a mapping of substrings that tile the string to their repetition count."""
    result: dict[str, int] = {}
    n: int = len(id_)

    # Only consider widths up to n // 2
    for width in range(1, (n // 2) + 1):
        # Only consider widths that evenly divide n
        if n % width != 0:
            continue

        # Get the candidate block and its (possible) repetitions
        block: str = id_[:width]
        repetitions: int = n // width

        # Check if repeating the block reconstructs the entire string.
        if block * repetitions == id_:
            result[block] = repetitions

    return result


id_ranges = read_data(DATA_FILE)
part_1 = 0
part_2 = 0
for id_range in id_ranges:
    id_range_split = id_range.split("-")
    for id_ in range(int(id_range_split[0]), 1 + int(id_range_split[1])):
        count = count_duplicates(str(id_))

        if 2 in count.values():
            part_1 += id_

        if count:
            part_2 += id_

print(part_1)
print(part_2)
