from typing import Dict, List, Optional, Set, Tuple
import re

Edges = Dict[str, Set[str]]
Fringe = List[str]

line_regex = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.")


def parse_line(line: str) -> Tuple[str, str]:
    match = line_regex.match(line)
    if match is None:
        raise Exception(f"Invalid line: {line}")
    src, tgt = match.groups()
    return (src, tgt)


def load_instructions(path: str) -> Tuple[Edges, Edges, Set[str]]:
    out_edges: Edges = {}
    in_edges: Edges = {}
    vertices: Set[str] = set()
    with open(path) as f:
        for line in f:
            src, tgt = parse_line(line.strip())
            if src not in out_edges:
                out_edges[src] = set()
            if tgt not in in_edges:
                in_edges[tgt] = set()
            out_edges[src].add(tgt)
            in_edges[tgt].add(src)
            vertices.add(src)
            vertices.add(tgt)
    return (in_edges, out_edges, vertices)


def topological_sort(in_edges: Edges, out_edges: Edges, vertices: Set[str]) -> str:
    traversal: List[str] = []
    fringe = set([v for v in vertices if
                     (v not in in_edges or len(in_edges[v]) == 0) and
                     v not in traversal])
    while len(fringe) > 0:
        current = min(fringe)
        traversal.append(current)
        fringe.remove(current)

        for tgt in out_edges.get(current, []):
            print(tgt, fringe, in_edges[tgt])
            if set(traversal) >= in_edges[tgt]:
                fringe.add(tgt)

    return ''.join(traversal)


def parallel_topological(in_edges: Edges, out_edges: Edges, vertices: Set[str], num_workers: int = 2, base_cost: int = 0) -> int:
    def cost(v: str) -> int:
        return base_cost + ord(v) - ord('A') + 1

    workers: List[Optional[Tuple[str, int]]] = [None] * num_workers
    traversal: List[str] = []

    fringe = set([v for v in vertices if
                 (v not in in_edges or len(in_edges[v]) == 0) and
                 v not in traversal])

    time = 0

    while len(fringe) > 0 or len(list(filter(lambda x: x is not None, workers))) > 0:
        for idx in range(0, num_workers):
            worker = workers[idx]
            print(worker, end='')
            if worker is not None and worker[1] == time:
                current = worker[0]
                traversal.append(current)

                for tgt in out_edges.get(current, []):
                    print(tgt, fringe, in_edges[tgt])
                    if set(traversal) >= in_edges[tgt]:
                        fringe.add(tgt)

                workers[idx] = None

            if workers[idx] is None and len(fringe) > 0:
                current = min(fringe)
                fringe.remove(current)
                workers[idx] = (current, time + cost(current))
        time += 1
        print(time)

    print(''.join(traversal))
    return time - 1


def part_1() -> None:
    in_edges, out_edges, vertices = load_instructions('../input/7')
    print(topological_sort(in_edges, out_edges, vertices))


def part_2() -> None:
    in_edges, out_edges, vertices = load_instructions('../input/7')
    print(parallel_topological(in_edges, out_edges, vertices, num_workers=5, base_cost=60))


if __name__ == '__main__':
    part_2()

