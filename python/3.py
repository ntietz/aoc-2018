from typing import Dict, List, Optional, Set, Tuple

Position = Tuple[int, int]
Size = Tuple[int,int]
ClaimId = str
Claim = Tuple[Position, Size, ClaimId]

def compute_overlap(claim1: Claim, claim2: Claim) -> Optional[Claim]:
    """Finds the claim which represents the overlap between these two claims."""
    if not does_overlap(claim1, claim2):
        return None
    return None # TODO


def does_overlap(claim1: Claim, claim2: Claim) -> bool:
    top_left: Position = claim1[0]
    bottom_right: Position = (claim1[0][0] + claim1[1][0], claim1[0][1] + claim1[1][1])

    return False # TODO


def naive_part1() -> Tuple[int, Optional[ClaimId]]:
    claims: List[Claim] = []
    overlappers: Dict[ClaimId, Set[ClaimId]] = {}
    with open('../input/3') as f:
        for line in f:
            claim_id, rest = line.strip().split(' @ ')
            pos, size = rest.split(': ')
            xpos, ypos = pos.split(',')
            xsize, ysize = size.split('x')
            claims.append(((int(xpos),int(ypos)), (int(xsize),int(ysize)), claim_id))
            overlappers[claim_id] = set()

    fabric: Dict[int, Dict[int, int]] = {}
    claimers: Dict[int, Dict[int, Set[ClaimId]]] = {}
    MAX_SIZE = 1000
    for x in range(0, MAX_SIZE):
        fabric[x] = {}
        claimers[x] = {}
        for y in range(0, MAX_SIZE):
            fabric[x][y] = 0
            claimers[x][y] = set()

    for claim in claims:
        for x in range(claim[0][0], claim[0][0] + claim[1][0]):
            for y in range(claim[0][1], claim[0][1] + claim[1][1]):
                fabric[x][y] += 1
                claimers[x][y].add(claim[2])

    count = 0
    for x in range(0, MAX_SIZE):
        for y in range(0, MAX_SIZE):
            if fabric[x][y] > 1:
                count += 1
                overlapped = claimers[x][y]
                for each in overlapped:
                    for other in overlapped.difference({each}):
                        overlappers[each].add(other)

    for claimId in overlappers:
        if len(overlappers[claimId]) == 0:
            return (count, claimId)
    return (count, None)

if __name__ == '__main__':
    print(f'Day 3, both parts: {naive_part1()}')


