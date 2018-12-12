from typing import List, Tuple


def load_input(path: str, pad: int = 24) -> Tuple[str, int, List[Tuple[str, str]]]:
    with open(path) as f:
        lines = f.read().split('\n')

        initial = '.'*pad + lines[0].split(': ')[1] + '.'*pad

        instructions: List[Tuple[str,str]] = []
        for line in lines[2:]:
            if len(line.strip()) == 0:
                continue
            pattern, result = line.split(' => ')
            instructions.append((pattern, result))

    return (initial, pad, instructions)


def find_all(s: str, pattern: str) -> List[int]:
    matches = []
    previous = s.find(pattern)
    while previous >= 0:
        matches.append(previous)
        previous = s.find(pattern, previous+1)
    return matches


def iterate(state: str, instructions: List[Tuple[str,str]]) -> str:
    updated_state = ['.']*len(state)
    for pattern, result in instructions:
        matches = find_all(state, pattern)
        for idx in matches:
            updated_state[idx+2] = result
    return ''.join(updated_state)


def score_state(state: str, pad: int) -> int:
    matches = find_all(state, '#')
    return sum(matches) - pad*len(matches)


def part1() -> None:
    state, pad, instructions = load_input('../input/12')
    for idx in range(0, 20):
        state = iterate(state, instructions)
    print(state)
    print(score_state(state, pad))


def part2() -> None:
    state, pad, instructions = load_input('../input/12', pad=10000)
    prev_score = score_state(state, pad)
    iters = 1000
    for idx in range(0, iters):
        state = iterate(state, instructions)
        score = score_state(state, pad)
        diff = score - prev_score
        #print(idx, score, score - prev_score)
        prev_score = score
    print(score + diff * (50000000000 - iters))


part1()
part2()

