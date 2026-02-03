from pathlib import Path
from loguru import logger

input_example_p1_path = Path(__file__).parent / "example_input_p1.txt"
input_example_p1_text = input_example_p1_path.read_text()
input_example_p2_path = Path(__file__).parent / "example_input_p2.txt"
input_example_p2_text = input_example_p2_path.read_text()
input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()

type Vec = tuple[int, int]


def get_char(text_grid: list[str], pos: Vec) -> str:
    # Out of grid
    if not (0 <= pos[1] < len(text_grid)) or not (0 <= pos[0] < len(text_grid[0])):
        return ""
    return text_grid[pos[1]][pos[0]]


def add_vec(v1: Vec, v2: Vec) -> Vec:
    return v1[0] + v2[0], v1[1] + v2[1]


def solve(input_text: str) -> tuple[int, int]:
    answer_part1 = answer_part2 = 0
    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_p1 = solve(input_example_p1_text)
    answer_example_part1 = solution_example_p1[0]
    logger.info(f"The solution for the example for part1 is: {answer_example_part1 = }")
    assert answer_example_part1 == 19114

    # Part 2
    solution_example_p2 = solve(input_example_p2_text)
    answer_example_part2 = solution_example_p2[1]
    logger.info(f"The solution for the example for part2 is: {answer_example_part2 = }")
    assert answer_example_part2 == 0

    solution = solve(input_text)
    answer_part1 = solution[0]
    logger.info(f"The solution for the part1 is: {answer_part1 = }")
    answer_part2 = solution[1]
    logger.info(f"The solution for the part2 is: {answer_part2 = }")


if __name__ == "__main__":
    main()
