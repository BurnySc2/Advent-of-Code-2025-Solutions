from functools import cache
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve(input_text: str) -> tuple[int, int]:
    lines = input_text.splitlines()
    words = [w.strip() for w in lines[0].split(",")]
    sequences = lines[2:]

    @cache
    def dfs(remaining_sequence: str) -> int:
        count = 0
        for word in words:
            if len(remaining_sequence) <= len(word):
                if remaining_sequence == word:
                    count += 1
                continue
            if remaining_sequence.startswith(word):
                count += dfs(remaining_sequence[len(word) :])
        return count

    answer_part1 = 0
    answer_part2 = 0
    for sequence in sequences:
        count = dfs(sequence)
        if 0 < count:
            answer_part1 += 1
            answer_part2 += count

    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 6

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 16

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
