from typing import List, Tuple

Recipes = List[int]
Elves = List[int]

#@profile
#def iterate(recipes: Recipes, elves: Elves) -> Tuple[Recipes,Elves]:
#    new_recipes = recipes + [int(c) for c in str(sum([recipes[elf] for elf in elves]))]
#    new_elves = [(1 + recipes[elf] + elf) % len(new_recipes) for elf in elves]
#    return new_recipes, new_elves

@profile
def iterate(recipes: Recipes, elves: Elves) -> None:
    value = 0
    for elf in elves:
        value += recipes[elf]
    new_recipes = [int(c) for c in str(value)]
    for r in new_recipes:
        recipes.append(r)
    for idx in range(0, len(elves)):
        elf = elves[idx]
        elves[idx] = (1 + recipes[elf] + elf) % len(recipes)


@profile
def repeat_iterations(recipes: Recipes, elves: Elves, num_recipes: int) -> None:
    #idx = 0
    while len(recipes) < num_recipes:
        #if idx % 10000 == 0:
        #    print(idx)
        iterate(recipes, elves)
        #idx += 1


def solve_part1(num_recipes: int) -> None:
    recipes = [3,7]
    elves = [0,1]
    cutoff = num_recipes + 10
    repeat_iterations(recipes, elves, cutoff)
    print(''.join(map(str, recipes[num_recipes:cutoff])))


@profile
def solve_part2(query: str, batch_size: int = 1000000) -> None:
    recipes = [3,7]
    elves = [0,1]

    for iteration in range(1, 100000):
        print(iteration)
        repeat_iterations(recipes, elves, batch_size * iteration)
        s = ''.join(map(str, recipes))
        loc = s.find(query)
        if loc >= 0:
            print(loc)
            return



#solve_part1(5)
#solve_part1(18)
#solve_part1(2018)
#solve_part1(380621)
#solve_part2('51589')
#solve_part2('01245')
#solve_part2('92510')
#solve_part2('59414')
solve_part2('380621')

