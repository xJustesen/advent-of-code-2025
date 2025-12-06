from pathlib import Path


def load_ranges_and_values(path: str) -> tuple[list[list[int]], list[int]]:
    """Load ranges before blank line and numbers after blank line from text file."""
    text = Path(path).read_text().strip("\n")

    # Split on first blank line
    before, after = text.split("\n\n", maxsplit=1)

    ranges = []
    values = []

    # Parse ranges
    for line in before.splitlines():
        start_s, end_s = line.split("-")
        ranges.append([int(start_s), int(end_s)])

    # Parse numbers after the blank line
    for line in after.splitlines():
        values.append(int(line))

    return ranges, values


def consolidate(intervals: list[list[int]]) -> list[list[int]]:
    """Consolidate overlapping intervals into non-overlapping intervals."""
    intervals_sorted = sorted(intervals, key=lambda x: x[0])
    consolidated = [intervals_sorted[0]]

    for current in intervals_sorted[1:]:
        last_consolidated = consolidated[-1]

        if current[0] > last_consolidated[-1]:
            # If not overlapping append the current interval
            consolidated.append(current)
        else:
            # Otherwise update the upper-bound of the last consolidated interval
            last_consolidated[1] = max(current[1], last_consolidated[1])

    return consolidated


# Example usage:
ranges, values = load_ranges_and_values("day5/input.txt")
# print(len(ranges), ranges[:5])
# print(len(values), values[:5])
# ranges = [(3, 5), (10, 14), (12, 18), (16, 20)]
# values = [1, 5, 8, 11, 17, 32]
ranges = consolidate(ranges)

# PART 1
count = 0
for value in values:
    for range_ in ranges:
        if value >= range_[0] and value <= range_[1]:
            count += 1
            break
print(count)


# PART 2
count = 0
for range_ in ranges:
    count += 1 + range_[1] - range_[0]
print(count)
