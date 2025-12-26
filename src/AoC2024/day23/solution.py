from itertools import combinations, product
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve(input_text: str) -> tuple[int, str]:
    lines = sorted(
        (c1, c2) for c1, c2 in [i.split("-") for i in input_text.splitlines()]
    )
    connections: set[tuple[str, ...]] = {(c1, c2) for c1, c2 in lines} | {
        (c2, c1) for c1, c2 in lines
    }
    nodes = sorted({c1 for c1, _ in connections})

    # Part 1
    answer_part1 = 0
    part2_candidates = set[tuple[str, ...]]()
    for c1, c2, c3 in combinations(nodes, 3):
        if (
            (c1, c2) in connections
            and (c1, c3) in connections
            and (c2, c3) in connections
        ):
            if any(c.startswith("t") for c in [c1, c2, c3]):
                answer_part1 += 1
            part2_candidates.add((c1, c2, c3))

    # Part 2
    answer_part2 = ""
    # Start with sets of four (three already checked in part1)
    for _ in range(4, len(nodes)):
        plus_one_length_part2_candidates = set[tuple[str, ...]]()
        for combo, c2 in product(part2_candidates, nodes):
            is_interconnected = True
            for c1 in combo:
                if (c1, c2) not in connections:
                    is_interconnected = False
                    break
            if is_interconnected:
                # Add sorted to set to avoid duplicates
                plus_one_length_part2_candidates.add(tuple(sorted(list(combo) + [c2])))

        if part2_candidates:
            # Keep track of best candidate so far
            answer_part2 = ",".join(list(part2_candidates)[0])
        else:
            break
        part2_candidates = plus_one_length_part2_candidates

    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 7

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == "co,de,ka,ta"

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
