# your_module.py
from itertools import groupby
from typing import Generator


def parse_with_whitespace(path: str) -> list[list[str]]:
    """Parse a fixed-width, space-separated column file into column-aligned strings."""

    def _separator_mask(grid: list[str]) -> list[bool]:
        """Return a mask where True marks columns that have spaces in all rows."""
        if not grid:
            return []
        width = len(grid[0])
        return [all(row[col] == " " for row in grid) for col in range(width)]

    def _column_ranges(sperator_mask) -> list[tuple[int, int]]:
        """Find the start and end indices of non-separator columns."""
        column_ranges: list[tuple[int, int]] = []
        for is_sep, group in groupby(enumerate(sperator_mask), key=lambda x: x[1]):
            if is_sep:
                continue
            indices = [idx for idx, _ in group]
            column_ranges.append((indices[0], indices[-1]))
        return column_ranges

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f if line.strip()]

    is_separator = _separator_mask(lines)
    column_ranges = _column_ranges(is_separator)

    columns: list[list[str]] = []
    for start, end in column_ranges:
        col_values = [row[start : end + 1] for row in lines]
        columns.append(col_values)

    return columns


def convert(numbers: list[str]) -> Generator[str, None, None]:
    width = len(numbers[0])
    return ("".join([x[i].strip(" ") for x in numbers]) for i in range(width))


data = parse_with_whitespace("day6/input.txt")

# PART 1+2
part1 = 0
part2 = 0
for problem in data:
    opr = problem[-1]
    numbers = problem[:-1]
    part1 += eval(opr.join(numbers))
    part2 += eval(opr.join(convert(numbers)))
print(part1)
print(part2)
