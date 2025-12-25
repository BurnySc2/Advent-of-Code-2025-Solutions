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
    grid = [list(row) for row in input_text.splitlines() if "#" in row]

    directions_dict: dict[str, Vec] = {
        "v": (0, 1),
        "^": (0, -1),
        "<": (-1, 0),
        ">": (1, 0),
    }
    robot_movements = "".join(
        row for row in input_text.splitlines() if any(char in row for char in "><^v")
    )
    robot_position = next(
        (x, y)
        for y, row in enumerate(grid)
        for x, value in enumerate(row)
        if value == "@"
    )

    def move_item(position: Vec, direction: Vec) -> bool:
        # Out of bounds
        if get_char(grid, position) is None:
            return False
        # Current position is empty
        if get_char(grid, position) == "#":
            return False
        if get_char(grid, position) == ".":
            return True
        new_pos = add_vec(position, direction)
        if move_item(new_pos, direction):
            grid[new_pos[1]][new_pos[0]] = grid[position[1]][position[0]]
            grid[position[1]][position[0]] = "."
            return True
        return False

    def get_score():
        score = 0
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value != "O":
                    continue
                score += 100 * y + x
        return score

    for move in robot_movements:
        direction = directions_dict[move]
        new_pos = add_vec(robot_position, direction)
        moved = move_item(robot_position, direction)
        if moved:
            robot_position = new_pos
            # for row in grid:
            #     print("".join(row))
            # print()

    answer_part1 = get_score()

    # for row in grid:
    #     print("".join(row))

    return answer_part1, 0


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
    assert answer_example_part2 == 7036

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
