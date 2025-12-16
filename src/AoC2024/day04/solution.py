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


def solve_part1(text_grid: list[str], pos: Vec) -> int:
    offsets: list[Vec] = [
        (x, y) for y in range(-1, 2) for x in range(-1, 2) if x != 0 or y != 0
    ]
    count = 0
    for offset in offsets:
        for i, char in enumerate("XMAS"):
            new_pos = (pos[0] + i * offset[0], pos[1] + i * offset[1])
            if get_char(text_grid, new_pos) != char:
                break
            # Last char reached
            if i == len("XMAS") - 1:
                count += 1
    return count


def solve_part2(text_grid: list[str], pos: Vec) -> int:
    if get_char(text_grid, pos) != "A":
        return 0
    offsets1: list[Vec] = [(-1, -1), (1, 1)]
    offsets2: list[Vec] = [(1, -1), (-1, 1)]

    def has_mas(text_grid: list[str], pos: Vec, offsets: list[Vec]):
        diag1 = [
            get_char(text_grid, (pos[0] + offsets[0][0], pos[1] + offsets[0][1])),
            get_char(text_grid, (pos[0] - offsets[0][0], pos[1] - offsets[0][1])),
        ]
        diag2 = [
            get_char(text_grid, (pos[0] + offsets[0][0], pos[1] + offsets[0][1])),
            get_char(text_grid, (pos[0] - offsets[0][0], pos[1] - offsets[0][1])),
        ]
        has_diag_match = all("".join(sorted(diag)) == "MS" for diag in [diag1, diag2])
        return has_diag_match

    if all(has_mas(text_grid, pos, offsets) for offsets in [offsets1, offsets2]):
        return 1
    return 0


def solve(input_text: str) -> tuple[int, int]:
    parsed = input_text.splitlines()

    answer_part1 = sum(
        solve_part1(parsed, (x, y))
        for y in range(len(parsed))
        for x in range(len(parsed[0]))
    )
    answer_part2 = sum(
        solve_part2(parsed, (x, y))
        for y in range(len(parsed))
        for x in range(len(parsed[0]))
    )
    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 18

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 9

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
