from typing import Iterator, List, NamedTuple, Optional, Tuple


class Point(NamedTuple):
    x: int
    y: int


class Coord(NamedTuple):
    x: int
    y: int
    num: int

    @staticmethod
    def from_line(line: str, num: int) -> 'Coord':
        x, y = line.strip().split(', ')
        return Coord(int(x), int(y), num)


class GridCell():
    color: Optional[int]
    distance: int = 1000000

    def __init__(self, color: Optional[int], distance: int = 1000000):
        self.color = color
        self.distance = distance

    def __repr__(self):
        return f'GridCell(color={self.color}, distance={self.distance})'

    def set_color(self, color):
        self.color = color

    def set_distance(self, distance):
        self.distance = distance

Grid = List[List[GridCell]]


def load_coords(path: str) -> List[Coord]:
    coords = []
    with open(path) as f:
        num = 0
        for line in f:
            coords.append(Coord.from_line(line, num))
            num += 1
    return coords


def bounding_grid(coords: List[Coord]) -> Grid:
    max_x = max(map(lambda coord: coord.x, coords))
    max_y = max(map(lambda coord: coord.y, coords))

    grid: Grid = []
    for x in range(0, max_x + 2):
        row = []
        for y in range(0, max_y + 2):
            row.append(GridCell(None))
        grid.append(row)

    for coord in coords:
        grid[coord.x][coord.y] = GridCell(coord.num, 0)

    return grid


def print_grid(grid: Grid) -> None:
    for row in grid:
        for cell in row:
            if cell.color is not None:
                print(cell.color, end='')
            else:
                print('.', end='')
        print('')


def color_grid(grid: Grid) -> Tuple[Grid, bool]:
    max_x = len(grid)
    max_y = len(grid[0])

    new_grid: Grid = []
    for x in range(0, max_x):
        row = []
        for y in range(0, max_y):
            row.append(grid[x][y])
        new_grid.append(row)

    changed = False

    for x in range(0, len(grid)):
        for y in range(0, len(grid[x])):
            if grid[x][y].color is not None:
                continue
            neighbors = find_neighbors(x, y, max_x, max_y, grid)
            min_distance = min(map(lambda n: n.distance, neighbors))
            closest_neighbors = [n.color for n in neighbors if n.distance == min_distance]
            if len(set(closest_neighbors)) == 1 and min_distance < 1000000:
                closest_color = closest_neighbors[0]
                new_grid[x][y] = GridCell(closest_color, min_distance + 1)
                changed = True

    return new_grid, changed


def find_neighbors(x: int, y: int, max_x: int, max_y: int, grid: Grid) -> List[GridCell]:
    def in_bounds(pair: Tuple[int, int]) -> bool:
        return 0 <= pair[0] < max_x and 0 <= pair[1] < max_y
    def get_neighbor(pair: Tuple[int, int]) -> GridCell:
        return grid[pair[0]][pair[1]]
    potentials = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    available = filter(in_bounds, potentials)
    cells = list(map(get_neighbor, available))
    return cells


def size(grid: Grid, color: int) -> int:
    max_x = len(grid)
    max_y = len(grid[0])

    for x in range(0, max_x):
        if grid[x][0].color == color or grid[x][max_y-1].color == color:
            return -1
    for y in range(0, max_y):
        if grid[0][y].color == color or grid[max_x-1][y].color == color:
            return -1

    count = 0

    for row in grid:
        for cell in row:
            if cell.color == color:
                count += 1

    return count

def part_1() -> None:
    coords = load_coords('../input/6')
    colors = [color for color in range(0, len(coords))]
    grid = bounding_grid(coords)
    #print_grid(grid)
    changed = True
    while changed:
        grid, changed = color_grid(grid)

    #print()
    #print_grid(grid)

    for color in colors:
        print(f'{color}: {size(grid, color)}')

    largest = max(map(lambda c: size(grid, c), colors))
    print(largest)


def total_distance(point: Point, coords: List[Coord]) -> int:
    total = 0
    for coord in coords:
        total += abs(point.x - coord.x) + abs(point.y - coord.y)
    #print(Point, total)
    return total


def region_size(grid: Grid, coords: List[Coord], cutoff: int = 32) -> int:
    max_x = len(grid)
    max_y = len(grid[0])

    count = 0

    for x in range(0, len(grid)):
        for y in range(0, len(grid[x])):
            count += 1 if total_distance(Point(x,y), coords) < cutoff else 0

    return count


def part_2(test: bool = False) -> None:
    path = '../input/6' if not test else '../input/6_test'
    cutoff = 10000 if not test else 32
    coords = load_coords(path)
    grid = bounding_grid(coords)
    print(region_size(grid, coords, cutoff))

if __name__ == '__main__':
    part_2()

