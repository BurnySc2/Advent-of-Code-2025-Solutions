import re
from functools import reduce
from operator import mul
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve(input_text: str, width: int, height: int) -> tuple[int, int]:
    loops = 100
    center = width // 2, height // 2

    robot_count_quadrant = [0, 0, 0, 0]

    for line in input_text.splitlines():
        pos_x, pos_y, v_x, v_y = re.match(
            r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line
        ).groups()
        pos_x, pos_y, v_x, v_y = list(map(int, [pos_x, pos_y, v_x, v_y]))

        final_pos_x = (pos_x + v_x * loops) % width
        final_pos_y = (pos_y + v_y * loops) % height
        if final_pos_x == center[0] or final_pos_y == center[1]:
            continue
        quadrant_horizontal = 2 * final_pos_x // width
        quadrant_vertical = 2 * final_pos_y // height
        quadrant = 2 * quadrant_horizontal + quadrant_vertical
        assert quadrant_horizontal < 2
        assert quadrant_vertical < 2
        assert 0 <= quadrant < 4
        robot_count_quadrant[quadrant] += 1
    answer_part1 = reduce(mul, robot_count_quadrant)

    return answer_part1, 0


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text, 11, 7)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 12

    solution = solve(input_text, 101, 103)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    # TODO Part 2 not done
    solution_example_part2 = solve(input_example_text, 11, 7)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 875318608908

    solution_part2 = solve(input_text, 101, 103)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
