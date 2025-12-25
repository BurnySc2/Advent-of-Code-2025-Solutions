import re
from functools import reduce
from operator import mul
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

type Vec = tuple[int, int]


def add_vec(v1: Vec, v2: Vec) -> Vec:
    return v1[0] + v2[0], v1[1] + v2[1]


def solve(input_text: str, width: int, height: int) -> tuple[int, int]:
    loops = 100
    center = width // 2, height // 2

    robots = list[tuple[int, int, int, int]]()
    for line in input_text.splitlines():
        pos_x, pos_y, v_x, v_y = re.match(
            r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line
        ).groups()  # pyright: ignore[reportOptionalMemberAccess]
        pos_x, pos_y, v_x, v_y = list(map(int, [pos_x, pos_y, v_x, v_y]))
        robots.append((pos_x, pos_y, v_x, v_y))

    robot_count_quadrant: list[int] = [0, 0, 0, 0]

    def calc_quadrants(loops: int) -> list[tuple[int, int]]:
        positions = list[tuple[int, int]]()
        for pos_x, pos_y, v_x, v_y in robots:
            final_pos_x = (pos_x + v_x * loops) % width
            final_pos_y = (pos_y + v_y * loops) % height
            positions.append((final_pos_x, final_pos_y))
            if final_pos_x == center[0] or final_pos_y == center[1]:
                continue
            quadrant_horizontal = 2 * final_pos_x // width
            quadrant_vertical = 2 * final_pos_y // height
            quadrant = 2 * quadrant_horizontal + quadrant_vertical
            assert quadrant_horizontal < 2
            assert quadrant_vertical < 2
            assert 0 <= quadrant < 4
            robot_count_quadrant[quadrant] += 1
        return positions

    _ = calc_quadrants(loops)
    answer_part1: int = reduce(mul, robot_count_quadrant)  # pyright: ignore[reportAny]

    loops = 0
    answer_part2 = -1
    while 100 < width:
        robot_count_quadrant = [0, 0, 0, 0]
        positions = calc_quadrants(loops)
        positions.sort(key=lambda i: (i[1], i[0]))

        most_count = list[int]()
        old_pos = -1, -1
        count = 0
        for pos in positions:
            if add_vec(old_pos, (1, 0)) == pos:
                count += 1
                most_count.append(count)
            else:
                count = 0
            old_pos = pos
        highest_in_a_row = max(most_count, default=0)

        if 10 < highest_in_a_row:
            # print grid
            grid = [["." for _ in range(width)] for _ in range(height)]
            for pos in positions:
                grid[pos[1]][pos[0]] = "#"
            for row in grid:
                print("".join(row))
            answer_part2 = loops
            break
        loops += 1

    return answer_part1, answer_part2


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
    # solution_example_part2 = solve(input_example_text, 11, 7)
    # answer_example_part2 = solution_example_part2[1]
    # print(f"The solution for the example for part2 is: {answer_example_part2=}")
    # assert answer_example_part2 == 875318608908

    solution_part2 = solve(input_text, 101, 103)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
