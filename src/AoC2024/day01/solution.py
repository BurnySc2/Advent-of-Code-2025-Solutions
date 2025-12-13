from collections import Counter
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve(input_text: str) -> tuple[int, int]:
    # Part 1
    xs: list[int] = []
    ys: list[int] = []
    for x, y in (line.split() for line in input_text.splitlines()):
        xs.append(int(x))
        ys.append(int(y))
    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)
    part1_solution = 0
    for x, y in zip(xs_sorted, ys_sorted):
        part1_solution += abs(x - y)

    # Part 2
    counter = Counter(ys)
    part2_solution = sum(x * counter[x] for x in xs)
    return part1_solution, part2_solution


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 11

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 31

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
