from typing import Iterator, List, Tuple, Union


Metadata = int
Tree = Tuple[List['Tree'], List[Metadata]] # type: ignore


def get_entries(test: bool = True) -> List[int]:
    path = '../input/8' if not test else '../input/8_test'
    with open(path) as f:
        content = f.read()
        parts = content.split()
        return [int(x) for x in parts]


def parse_tree(raw: List[int]) -> Tuple[Tree, List[int]]:
    num_children, num_metadata, *remainder = raw
    children: List[Tree] = []
    for idx in range(0, num_children):
        child, remainder = parse_tree(remainder)
        children.append(child)
    return ((children, remainder[:num_metadata]), remainder[num_metadata:])


def metadata(tree: Tree) -> Iterator[int]:
    for child in tree[0]:
        for each in metadata(child):
            yield each
    for each in tree[1]:
        yield each


def checksum_part2(tree: Tree) -> int:
    if len(tree[0]) == 0:
        return sum(tree[1])
    total = 0
    for num in tree[1]:
        if num-1 < len(tree[0]):
            child = tree[0][num-1]
            total += checksum_part2(child)
    return total



def part_1(test: bool = True) -> None:
    raw_tree = get_entries(test)
    tree, _ = parse_tree(raw_tree)
    print(sum(metadata(tree)))


def part_2(test: bool = True) -> None:
    raw_tree = get_entries(test)
    tree, _ = parse_tree(raw_tree)
    print(checksum_part2(tree))


if __name__ == '__main__':
    part_1(False)
    part_2(False)
