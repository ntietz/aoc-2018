from typing import Dict, List, Iterator, Tuple


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


def num_differences(a: str, b: str) -> int:
    assert len(a) == len(b)
    return sum([1 if c != d else 0 for (c,d) in zip(a,b)])


def find_similar_ids() -> Tuple[str,str]:
    box_ids = [box_id for box_id in input_lines()]
    # Let's just brute-force it because we only have 30k combinations to check
    for first in range(0, len(box_ids)):
        for second in range(first+1, len(box_ids)):
            pair = (box_ids[first], box_ids[second])
            if num_differences(*pair) == 1:
                return pair
    raise Exception("No pair found")


def common_letters(a: str, b: str) -> str:
    assert len(a) == len(b)
    common = []
    for idx in range(0, len(a)):
        if a[idx] == b[idx]:
            common.append(a[idx])
    return ''.join(common)


def part2_solution() -> str:
    similar_pair = find_similar_ids()
    return common_letters(*similar_pair)


if __name__ == '__main__':
    print(f"Part 1: {checksum()}")
    print(f"Part 2: {part2_solution()}")
