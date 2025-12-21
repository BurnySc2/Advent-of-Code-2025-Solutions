import math
from pathlib import Path
import re

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def calc_coefficients(
    button_a_x: int,
    button_b_x: int,
    button_a_y: int,
    button_b_y: int,
    prize_x: int,
    prize_y: int,
) -> tuple[int, int]:
    # Solve
    # a*button_a_x + b*button_b_x = prize_x
    # a*button_a_y + b*button_b_y = prize_y

    multiple = math.lcm(button_b_x, button_b_y)
    factor1 = multiple // button_b_x
    factor2 = multiple // button_b_y

    # Solve for a
    # a * button_a_x * factor1 - a * button_a_y * factor2 = prize_x * factor1 - prize_y * factor2
    a = (prize_x * factor1 - prize_y * factor2) // (
        button_a_x * factor1 - button_a_y * factor2
    )
    # Solve for b
    b = (prize_x - a * button_a_x) // button_b_x

    # Validate
    equation1_validate = a * button_a_x + b * button_b_x == prize_x
    equation2_validate = a * button_a_y + b * button_b_y == prize_y
    if not all([equation1_validate, equation2_validate]):
        return -1, -1
    return a, b


def solve(input_text: str) -> tuple[int, int]:
    lines = input_text.splitlines()

    answer_part1 = 0
    answer_part2 = 0

    for i in range(0, len(lines), 4):
        button_a_x, button_a_y = re.search(r"X\+(\d+), Y\+(\d+)", lines[i]).groups()  # pyright: ignore[reportOptionalMemberAccess]
        button_b_x, button_b_y = re.search(r"X\+(\d+), Y\+(\d+)", lines[i + 1]).groups()  # pyright: ignore[reportOptionalMemberAccess]
        prize_x, prize_y = re.search(r"X=(\d+), Y=(\d+)", lines[i + 2]).groups()  # pyright: ignore[reportOptionalMemberAccess]

        # All values are >0
        assert button_a_x != "0"
        assert button_a_y != "0"
        assert button_b_x != "0"
        assert button_b_y != "0"

        a, b = calc_coefficients(
            int(button_a_x),
            int(button_b_x),
            int(button_a_y),
            int(button_b_y),
            int(prize_x),
            int(prize_y),
        )
        if 0 <= a and 0 <= b:
            answer_part1 += 3 * a + 1 * b

        a_part2, b_part2 = calc_coefficients(
            int(button_a_x),
            int(button_b_x),
            int(button_a_y),
            int(button_b_y),
            int(prize_x) + 10000000000000,
            int(prize_y) + 10000000000000,
        )
        if 0 <= a_part2 and 0 <= b_part2:
            answer_part2 += 3 * a_part2 + 1 * b_part2

    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 480

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 875318608908

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
