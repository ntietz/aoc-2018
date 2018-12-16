from typing import List, Tuple


def load_map(path: str) -> Tuple[List[List[str]], List[Tuple[Tuple[int, int], str, int]]]:
    lines: List[List[str]] = []
    with open(path) as f:
        for line in f:
            lines.append(list(line.strip('\n')))

    carts: List[Tuple[Tuple[int,int], str, int]] = []
    for row in range(0, len(lines)):
        for col in range(0, len(lines[row])):
            if lines[row][col] in {'<', '>'}:
                direction = lines[row][col]
                lines[row][col] = '-'
                carts.append(((row,col), direction, 0))
            elif lines[row][col] in {'^', 'v'}:
                direction = lines[row][col]
                lines[row][col] = '|'
                carts.append(((row,col), direction, 0))
    return lines, carts


changes = {
    'v': {
        '/': '<',
        '\\': '>'
    },
    '^': {
        '/': '>',
        '\\': '<'
    },
    '>': {
        '/': '^',
        '\\': 'v'
    },
    '<': {
        '/': 'v',
        '\\': '^'
    }
}

turns = {
    'v': {
        0: '>',
        1: 'v',
        2: '<'
    },
    '>': {
        0: '^',
        1: '>',
        2: 'v'
    },
    '^': {
        0: '<',
        1: '^',
        2: '>'
    },
    '<': {
        0: 'v',
        1: '<',
        2: '^'
    }
}


def move_cart(lines: List[List[str]], position: Tuple[int,int], direction: str, count: int) -> Tuple[Tuple[int,int], str, int]:
    cur = lines[position[0]][position[1]]

    new_dir = direction
    new_dir = changes[direction][cur] if cur in {'/','\\'} else new_dir
    if cur == '+':
        new_dir = turns[new_dir][count]
        count = (count + 1) % 3

    row, col = position
    if new_dir == 'v':
        row += 1
    elif new_dir == '^':
        row -= 1
    elif new_dir == '<':
        col -= 1
    elif new_dir == '>':
        col += 1
    new_pos = (row,col)

    #print(len(lines), len(lines[0]))
    #print('\n===')
    #print(position, direction)
    #print('cur', position, direction, lines[position[0]][position[1]])
    #print(new_pos)

    #print('new', new_pos, new_dir)
    #print(lines[new_pos[0]])
    new_spot = lines[new_pos[0]][new_pos[1]]
    #print('new', new_pos, new_dir, new_spot)

    return new_pos, new_dir, count


def print_carts(lines: List[List[str]], carts: List[Tuple[Tuple[int,int], str, int]]) -> None:
    lines = list(map(lambda line: list(line), lines))
    for position, direction, count in carts:
        lines[position[0]][position[1]] = direction
    for line in lines:
        print(''.join(line))


def sort_key(cart: Tuple[Tuple[int,int],str,int]) -> List[int]:
    return list(cart[0])#[-1::-1]


def compute(path: str) -> None:
    lines, carts = load_map(path)

    collided = False
    ticks = 0
    while not collided:
        updated_carts = []
        carts.sort(key=sort_key)
        positions = [cart[0] for cart in carts]
        for idx, (position, direction, count) in enumerate(carts):
            updated = move_cart(lines, position, direction, count)
            updated_carts.append(updated)
            positions[idx] = updated[0]
            for jdx, position in enumerate(positions):
                if jdx == idx:
                    continue
                if updated[0] == position:
                    x,y = position
                    print(f'collided at {y},{x}')
                    collided = True
                    return
        ticks += 1
        carts = updated_carts

def compute_2(path: str) -> None:
    lines, carts = load_map(path)

    ticks = 0
    while len(carts) > 1:
        updated_carts: List[Tuple[Tuple[int,int], str, int]] = []
        carts.sort(key=sort_key)
        alive = list(map(lambda cart: True, carts))
        positions = list(map(lambda cart: cart[0], carts))
        for idx, (position, direction, count) in enumerate(carts):
            if not alive[idx]:
                updated_carts.append((position, direction, count))
                continue
            updated = move_cart(lines, position, direction, count)
            updated_carts.append(updated)
            positions[idx] = updated[0]
            for jdx, position in enumerate(positions):
                if jdx == idx:
                    continue
                if updated[0] == position:
                    x,y = position
                    #print(f'collided at {y},{x}')
                    alive[idx] = False
                    alive[jdx] = False
        survivors = []
        for status, cart in zip(alive, updated_carts):
            if status:
                survivors.append(cart)
        ticks += 1
        carts = survivors
    print(f'{carts[0][0][1]},{carts[0][0][0]}')


compute('../input/13_test')
compute('../input/13')
compute('../input/13_test_2')
compute_2('../input/13_test_2')
compute_2('../input/13')

