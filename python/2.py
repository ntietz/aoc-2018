from typing import Dict, List, Iterator


def input_lines() -> Iterator[str]:
    path = '../input/2'
    with open(path) as f:
        for line in f:
            yield line.strip()


def letter_freqs(line: str) -> Dict[str, int]:
    freqs: Dict[str, int] = {}
    for c in line:
        if c not in freqs:
            freqs[c] = 0
        freqs[c] += 1
    return freqs


def invert_freqs(freqs: Dict[str, int]) -> Dict[int, List[str]]:
    inverse: Dict[int, List[str]] = {}
    for k,v in freqs.items():
        if v not in inverse:
            inverse[v] = []
        inverse[v].append(k)
    return inverse


def checksum() -> int:
    num_2 = 0
    num_3 = 0
    for line in input_lines():
        inverse_freqs = invert_freqs(letter_freqs(line))
        num_2 += 1 if 2 in inverse_freqs else 0
        num_3 += 1 if 3 in inverse_freqs else 0
    return num_2 * num_3


if __name__ == '__main__':
    print(f"Part 1: {checksum()}")
