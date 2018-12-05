import regex
import string


PATH = '../input/5'

pairs = regex.compile(r'([a-zA-Z])(?i:\1)(?<=[a-z][A-Z]|[A-Z][a-z])')


def reduce(polymer: str) -> str:
    previous = None
    while polymer != previous:
        previous = polymer
        polymer = regex.sub(pairs, '', polymer)
    return polymer


def part_1() -> int:
    with open(PATH) as f:
        polymer = f.read().strip()
        return len(reduce(polymer))


def part_2() -> int:
    with open(PATH) as f:
        original_polymer = f.read().strip()
        shortest = part_1()
        for a,A in zip(string.ascii_lowercase, string.ascii_uppercase):
            polymer = regex.sub(f'{a}|{A}', '', original_polymer)
            length = len(reduce(polymer))
            if length < shortest:
                shortest = length
        return shortest


if __name__ == '__main__':
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
