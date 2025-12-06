from dataclasses import dataclass, field
from typing import Literal


def read_data(path: str) -> list[str]:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return data


# Precomputed neighbour offsets (8 directions).
NEIGHBOUR_OFFSETS: tuple[tuple[int, int], ...] = tuple(
    (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if not (dx == 0 and dy == 0)
)


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def adjacent(self) -> list["Coord"]:
        return [Coord(self.x + dx, self.y + dy) for dx, dy in NEIGHBOUR_OFFSETS]


@dataclass(slots=True)
class Cell:
    coord: Coord
    symbol: Literal[".", "@"]

    def remove(self) -> None:
        self.symbol = "."


@dataclass(slots=True)
class Grid:
    cells: list[Cell]
    _lookup_table: dict[Coord, Cell] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initializes the internal coordinate-to-cell lookup table."""
        self._lookup_table = {cell.coord: cell for cell in self.cells}

    def get_cell_by_coord(self, coord: Coord) -> Cell | None:
        """Returns the cell for a coordinate or None if it does not exist."""
        return self._lookup_table.get(coord)


def count_matches(cell: Cell, grid: Grid) -> int:
    # Count the number of @ in adjacent cells
    coord = cell.coord

    # Get adjacent cells
    adj_cells = [grid.get_cell_by_coord(coord_) for coord_ in coord.adjacent()]

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
cells = grid.cells
count = 0
while True:
    cells_to_check = [cell for cell in cells if cell.symbol == "@"]

    # Compute which are valid
    matches = [(cell, count_matches(cell, grid) < 4) for cell in cells_to_check]

    # Count number of valid cells
    n_valid = sum(valid for _, valid in matches)

    # Break if finished
    if n_valid == 0:
        break

    # Increase total count of valid cells
    count += n_valid

    # Remove the valid cells
    for cell, is_valid in matches:
        if is_valid:
            cell.remove()

print(count)
