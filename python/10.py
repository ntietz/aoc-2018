from typing import List, NamedTuple, Tuple
import re


class Coord(NamedTuple):
    x: int
    y: int


class Vector(NamedTuple):
    x: int
    y: int


def parse_input(path: str) -> Tuple[List[Coord], List[Vector]]:
    parser = re.compile(r"position=<[ ]*([-]*[\d]*),[ ]*([-]*[\d]*)> velocity=<[ ]*([-]*[\d]*),[ ]*([-]*[\d]*)>")
    with open(path) as f:
        coords: List[Coord] = []
        vectors: List[Vector] = []
        for line in f:
            match = parser.match(line)
            if match is None:
                raise Exception(f"Invalid line: {line}")
            x, y, xd, yd = match.groups()
            coords.append(Coord(int(x), int(y)))
            vectors.append(Vector(int(xd), int(yd)))
        return (coords, vectors)


def time_to_zero(coords: List[Coord], vectors: List[Vector]) -> List[int]:
    xs = []
    ys = []
    for coord, vector in zip(coords, vectors):
        xiters = coord.x / vector.x if vector.x is not 0 else float('inf')
        yiters = coord.y / vector.y if vector.y is not 0 else float('inf')
        print(f'{xiters:10.4}, {yiters:10.4}')
        xs.append(xiters)
        ys.append(yiters)
        #print(coord, vector)
    print(max(xs), max(ys))
    print(min(xs), min(ys))
    return []


def coords_after(t: int, coords: List[Coord], vectors: List[Vector]) -> List[Coord]:
    return [Coord(coord.x + v.x*t, coord.y + v.y*t) for coord, v in zip(coords, vectors)]


def print_coords(coords: List[Coord]) -> None:
    xs = [coord.x for coord in coords]
    ys = [coord.y for coord in coords]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    grid = []
    for y in range(0, max_y - min_y + 1):
        grid.append([])
        for x in range(0, max_x - min_x + 1):
            grid[y].append('.')

    #    grid = [['.'] * (max_x - min_x)] * (max_y - min_y)

    for coord in coords:
        grid[coord.y - min_y][coord.x - min_x] = '#'

    for line in grid:
        print(''.join(line))


def part1_test():
    coords, vectors = parse_input('../input/10_test')
    #print(time_to_zero(coords, vectors))
    print_coords(coords)
    print()
    print_coords(coords_after(1, coords, vectors))
    print()
    print_coords(coords_after(2, coords, vectors))
    print()
    print_coords(coords_after(3, coords, vectors))


def part1():
    coords, vectors = parse_input('../input/10')
    #print(time_to_zero(coords, vectors))
    offset = 10567+89
    coords = coords_after(offset, coords, vectors)
    for idx in range(0, 500):
        print(idx+offset)
        print_coords(coords)
        input()
        coords = coords_after(1, coords, vectors)


if __name__ == '__main__':
    part1()
