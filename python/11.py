from typing import Dict, List, Tuple


def compute_score(x: int, y: int, serial_number: int) -> int:
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    power_level = int(str(power_level)[-3])
    return power_level - 5

#@profile
def best_subgrid(serial_number: int, size_lower: int = 3, size_upper: int = 4) -> Tuple[int,int,int]:
    X_LIMIT = 300
    Y_LIMIT = 300
    scores: List[Tuple[int, Tuple[int, int, int]]] = []

    grid: List[List[int]] = []

    high_score = 0
    coords = (0,0,0)

    for x in range(0, X_LIMIT):
        grid.append([])
        for y in range(0, Y_LIMIT):
            grid[x].append(compute_score(x+1, y+1, serial_number))

    for size in range(size_lower, size_upper):
        print(size)

        for y in range(0, Y_LIMIT - size):
            row_sums = [sum(grid[x][y:y+size]) for x in range(0, X_LIMIT)]

            for x in range(0, X_LIMIT-size):
                score = sum(row_sums[x:x+size])
                if score > high_score:
                    high_score = score
                    coords = (x+1,y+1,size)

    print(high_score)
    return coords


#print(best_subgrid(18))
#print(best_subgrid(18, 1, 301))
#print(best_subgrid(42, 1, 301))
print(best_subgrid(7400, 1, 301))

