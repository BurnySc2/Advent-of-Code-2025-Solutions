import itertools
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

type Vec = tuple[int, int]
type Antenna = tuple[int, int, str]


def get_antinodes(node1: Antenna, node2: Antenna) -> list[Vec]:
    distance = node2[0] - node1[0], node2[1] - node1[1]
    return [
        (node2[0] + distance[0], node2[1] + distance[1]),
        (node1[0] - distance[0], node1[1] - distance[1]),
    ]


def part2_get_antinodes(node1: Antenna, node2: Antenna) -> list[Vec]:
    distance = node2[0] - node1[0], node2[1] - node1[1]
    return [
        (node2[0] + distance[0] * factor, node2[1] + distance[1] * factor)
        for factor in range(-100, 100)
    ]


def solve(input_text: str) -> tuple[int, int]:
    grid = input_text.splitlines()
    antennas: list[Antenna] = [
        (x, y, value)
        for y, row in enumerate(grid)
        for x, value in enumerate(row)
        if value != "."
    ]

    def is_in_grid(vec: Vec) -> bool:
        return 0 <= vec[0] < len(grid[0]) and 0 <= vec[1] < len(grid)

    antinodes: list[Vec] = []
    for antenna1, antenna2 in itertools.combinations(antennas, 2):
        if antenna1[2] == antenna2[2]:
            antinodes.extend(get_antinodes(antenna1, antenna2))

    antinodes_part2: list[Vec] = []
    for antenna1, antenna2 in itertools.combinations(antennas, 2):
        if antenna1[2] == antenna2[2]:
            antinodes_part2.extend(part2_get_antinodes(antenna1, antenna2))

    answer_part1 = len(set(antinode for antinode in antinodes if is_in_grid(antinode)))
    answer_part2 = len(
        set(antinode for antinode in antinodes_part2 if is_in_grid(antinode))
    )
    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 14

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 34

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
