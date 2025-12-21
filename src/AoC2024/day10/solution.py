from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

# x, y
type Vec = tuple[int, int]


def get_char(text_grid: list[str], pos: Vec) -> str:
    # Out of grid
    if not (0 <= pos[1] < len(text_grid)) or not (0 <= pos[0] < len(text_grid[0])):
        return ""
    return text_grid[pos[1]][pos[0]]


def add_vec(v1: Vec, v2: Vec) -> Vec:
    return v1[0] + v2[0], v1[1] + v2[1]


def solve(input_text: str) -> tuple[int, int]:
    grid = input_text.splitlines()
    neighbors: list[Vec] = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    start_locations: list[Vec] = [
        (x, y)
        for y, row in enumerate(grid)
        for x, value in enumerate(row)
        if value == "0"
    ]
    locations_already_seen: set[Vec] = set()

    def dfs(current_position: Vec, current_value: int) -> int:
        char = get_char(grid, current_position)

        # Outside grid
        if char == "":
            return 0

        # Neighbor is not correct number
        if char == "." or current_value != int(char):
            return 0

        # End reached
        if current_value == 9:
            locations_already_seen.add(current_position)
            return 1

        # Split up
        return sum(
            dfs(add_vec(current_position, neighbor), current_value + 1)
            for neighbor in neighbors
        )

    answer_part1 = 0
    answer_part2 = 0
    for i in start_locations:
        answer_part2 += dfs(i, 0)
        answer_part1 += len(locations_already_seen)
        locations_already_seen.clear()

    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 36

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 81

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
