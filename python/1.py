from itertools import cycle
from typing import Iterator

def parse_line(line: str) -> int:
    return int(line)

def get_changes() -> Iterator[int]:
    path = '../input'
    with open(path) as f:
        for line in f:
            yield parse_line(line.strip())

def compute_frequency() -> int:
    """Solution for part 1"""
    freq = 0
    for change in get_changes():
        freq += change
    return freq

def find_repeat_frequency() -> int:
    changes = cycle(get_changes())
    freq = 0
    seen = {freq}
    for change in changes:
        freq += change
        if freq in seen:
            return freq
        seen.add(freq)
    raise Exception("No repeats found")

if __name__ == '__main__':
    print(compute_frequency())
    print(find_repeat_frequency())
