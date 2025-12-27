from collections.abc import Sequence
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

# x, y
type Vec = tuple[int, int]


def get_char[T](text_grid: Sequence[Sequence[T]], pos: Vec) -> T | None:
    # Out of grid
    if not (0 <= pos[1] < len(text_grid)) or not (0 <= pos[0] < len(text_grid[0])):
        return None
    return text_grid[pos[1]][pos[0]]


def add_vec(v1: Vec, v2: Vec) -> Vec:
    return v1[0] + v2[0], v1[1] + v2[1]


def solve(input_text: str) -> tuple[int, int]:
    grid_part1 = [list(row) for row in input_text.splitlines() if "#" in row]
    grid_part2 = [
        ["." for _ in range(len(grid_part1[0]) * 2)] for _ in range(len(grid_part1))
    ]
    for y, row in enumerate(grid_part1):
        for x, value in enumerate(row):
            left_value = "[" if value == "O" else value
            right_value = "]" if value == "O" else value
            if left_value == "@":
                right_value = "."
            grid_part2[y][2 * x] = left_value
            grid_part2[y][2 * x + 1] = right_value

    directions_dict: dict[str, Vec] = {
        "v": (0, 1),
        "^": (0, -1),
        "<": (-1, 0),
        ">": (1, 0),
    }
    robot_movements = "".join(
        row for row in input_text.splitlines() if any(char in row for char in "><^v")
    )
    robot_position_part1 = next(
        (x, y)
        for y, row in enumerate(grid_part1)
        for x, value in enumerate(row)
        if value == "@"
    )
    robot_position_part2 = next(
        (x, y)
        for y, row in enumerate(grid_part2)
        for x, value in enumerate(row)
        if value == "@"
    )

    def can_move(grid: list[list[str]], position: Vec, direction: Vec) -> bool:
        char = get_char(grid, position)
        if char is None or char == "#":
            return False
        if char == ".":
            return True
        new_pos = add_vec(position, direction)

        single_width = direction[1] == 0 or char not in "[]"
        if single_width:
            return can_move(grid, new_pos, direction)

        offset = (1, 0) if char == "[" else (-1, 0)
        new_pos2 = add_vec(new_pos, offset)
        return can_move(grid, new_pos, direction) and can_move(
            grid, new_pos2, direction
        )

    def move_item(grid: list[list[str]], position: Vec, direction: Vec) -> bool:
        if not can_move(grid, position, direction):
            return False
        char = get_char(grid, position)
        if char is None or char == ".":
            return False

        single_width = direction[1] == 0 or char not in "[]"

        # Move part 1
        new_pos = add_vec(position, direction)
        if single_width:
            _ = move_item(grid, new_pos, direction)
            grid[new_pos[1]][new_pos[0]] = grid[position[1]][position[0]]
            grid[position[1]][position[0]] = "."
            return True

        # Move part 2
        offset = (1, 0) if char == "[" else (-1, 0)
        new_pos2 = add_vec(new_pos, offset)
        _ = move_item(grid, new_pos, direction)
        _ = move_item(grid, new_pos2, direction)
        grid[new_pos[1]][new_pos[0]] = grid[position[1]][position[0]]
        grid[position[1]][position[0]] = "."

        position2 = add_vec(position, offset)
        grid[new_pos2[1]][new_pos2[0]] = grid[position2[1]][position2[0]]
        grid[position2[1]][position2[0]] = "."
        return True

    def get_score(grid: list[list[str]]):
        score = 0
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value not in "[O":
                    continue
                score += 100 * y + x
        return score

    for _debug_count, move in enumerate(robot_movements):
        direction = directions_dict[move]
        # Part 1
        new_pos = add_vec(robot_position_part1, direction)
        moved = move_item(grid_part1, robot_position_part1, direction)
        if moved:
            robot_position_part1 = new_pos
        # Part 2
        new_pos = add_vec(robot_position_part2, direction)
        moved = move_item(grid_part2, robot_position_part2, direction)
        if moved:
            robot_position_part2 = new_pos
            # for row in grid_part2:
            #     print("".join(row))
            # print(_debug_count)

    answer_part1 = get_score(grid_part1)
    answer_part2 = get_score(grid_part2)

    # for row in grid:
    #     print("".join(row))

    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 10092

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 9021

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
