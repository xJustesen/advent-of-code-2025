from dataclasses import dataclass
from typing import Literal


def read_data(path: str) -> list[str]:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return data


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass
class Cell:
    coord: Coord
    symbol: Literal[".", "@"]

    def remove(self) -> None:
        self.symbol = "."


@dataclass
class Grid:
    cells: list[Cell]

    def get_cell_by_coord(self, coord: Coord) -> Cell | None:
        try:
            return self.lookup_table[coord]
        except KeyError:
            return None

    def __post_init__(self) -> None:
        self.lookup_table = {cell.coord: cell for cell in self.cells}


def get_adjacent_coords(coord: Coord) -> list[Coord]:
    x = coord.x
    y = coord.y

    return [
        Coord(x - 1, y - 1),
        Coord(x - 1, y),
        Coord(x - 1, y + 1),
        Coord(x, y - 1),
        Coord(x, y + 1),
        Coord(x + 1, y - 1),
        Coord(x + 1, y),
        Coord(x + 1, y + 1),
    ]


def count_matches(cell: Cell, grid: Grid) -> int:
    # Count the number of @ in adjacent cells
    coord = cell.coord

    # Get adjacent cells
    adjacent_coords = get_adjacent_coords(coord)
    adj_cells = [grid.get_cell_by_coord(coord_) for coord_ in adjacent_coords]

    # Remove None entries
    adj_cells = [x for x in adj_cells if x is not None]

    # Return '@' occurences
    return sum(adj_cell.symbol == "@" for adj_cell in adj_cells)


# Read data and construct grid
data = read_data("day4/input.txt")

cells = []
for x, row in enumerate(data):
    for y, col in enumerate(row):
        cells.append(Cell(coord=Coord(x=x, y=y), symbol=col))  # type: ignore

grid = Grid(cells=cells)

# PART 1
cells_to_check = [cell for cell in cells if cell.symbol == "@"]
count = sum(count_matches(cell, grid) < 4 for cell in cells_to_check)
print(count)

# PART 2
count = 0
while True:
    cells_to_check = [cell for cell in cells if cell.symbol == "@"]
    matches = [(cell, count_matches(cell, grid) < 4) for cell in cells_to_check]

    # Count number of valid cells
    n_valid = sum(valid for _, valid in matches)

    # Break if finished
    if n_valid == 0:
        break

    # Increase total count of valid cells
    count += n_valid

    # Update the valid cells in the grid
    valid_cells = [cell for cell, is_valid in matches if is_valid]
    for cell in grid.cells:
        if cell in valid_cells:
            cell.remove()

print(count)
