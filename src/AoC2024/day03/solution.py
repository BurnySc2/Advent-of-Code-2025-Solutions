import re
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve(input_text: str) -> tuple[int, int]:
    part1_solution = 0
    part2_solution = 0
    part2_enabled = True
    for line in input_text.splitlines():
        do_matches = [
            i for i, _ in enumerate(line) if line[i : i + len("do()")] == "do()"
        ]
        dont_matches = [
            i for i, _ in enumerate(line) if line[i : i + len("don't()")] == "don't()"
        ]
        for match in re.finditer(r"mul\((\d+),(\d+)\)", line):
            a, b = match.groups()
            part1_solution += int(a) * int(b)

            match_index = match.regs[0][0]
            do_donts = sorted(
                [(i, True) for i in do_matches if i < match_index]
                + [(i, False) for i in dont_matches if i < match_index]
            )

            if do_donts and do_donts[-1][1] is True:
                part2_enabled = True
            if do_donts and do_donts[-1][1] is False:
                part2_enabled = False

            if part2_enabled:
                part2_solution += int(a) * int(b)
    return part1_solution, part2_solution


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 161

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 48

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
