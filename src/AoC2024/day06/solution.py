from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def get_char(grid: list[str], pos: tuple[int, int]) -> str:
    if not (0 <= pos[1] < len(grid)) or not (0 <= pos[0] < len(grid[0])):
        return ""
    return grid[pos[1]][pos[0]]


def solve(input_text: str) -> tuple[int, int]:
    """
    Doesnt solve:
    ......
    .^..#.
    ......
    #.....
    ...#..
    """
    grid = input_text.splitlines()
    start_position = next(
        (x, y)
        for y, row in enumerate(grid)
        for x, value in enumerate(row)
        if value == "^"
    )
    directions_map = {
        (0, -1): (1, 0),
        (1, 0): (0, 1),
        (0, 1): (-1, 0),
        (-1, 0): (0, -1),
    }

    current_position = start_position
    current_direction = (0, -1)
    positions_part1: dict[tuple[int, int], tuple[int, int]] = {
        current_position: current_direction
    }
    obstacles_part2: set[tuple[int, int]] = set()
    while 1:
        new_pos = (
            current_position[0] + current_direction[0],
            current_position[1] + current_direction[1],
        )
        char = get_char(grid, new_pos)

        # Info for part 2: check if position on the right has already been walked on in that direction
        part2_direction = directions_map[current_direction]
        for i in range(1, max(len(grid), len(grid[0]))):
            part2_pos = (
                current_position[0] + part2_direction[0] * i,
                current_position[1] + part2_direction[1] * i,
            )
            part2_char = get_char(grid, part2_pos)
            if part2_char not in {".", "^"}:
                break
            already_seen = (
                part2_pos in positions_part1
                and positions_part1[part2_pos] == part2_direction
            )
            if already_seen:
                obstacles_part2.add(new_pos)

        if current_position not in positions_part1:
            positions_part1[current_position] = current_direction
        if char == "#":
            current_direction = directions_map[current_direction]
            continue
        elif char == "":
            break
        current_position = new_pos
    return len(positions_part1), len(obstacles_part2)


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 41

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 6

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
