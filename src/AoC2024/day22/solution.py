from collections import deque
from functools import cache
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

type Vec = tuple[int, int]


def get_char(text_grid: list[str], pos: Vec) -> str:
    # Out of grid
    if not (0 <= pos[1] < len(text_grid)) or not (0 <= pos[0] < len(text_grid[0])):
        return ""
    return text_grid[pos[1]][pos[0]]


def add_vec(v1: Vec, v2: Vec) -> Vec:
    return v1[0] + v2[0], v1[1] + v2[1]


def solve(input_text: str) -> tuple[int, int]:
    @cache
    def generate_new_secret(secret_number: int) -> int:
        number = (secret_number * 64) ^ secret_number
        number = number % 16777216
        number = (number // 32) ^ number
        number = number % 16777216
        number = (number * 2048) ^ number
        number = number % 16777216
        return number

    solution_part1 = list[int]()
    # monkey_id, sequence_as_tuple[int], value as int
    part2_sequences = dict[int, dict[tuple[int, int, int, int], int]]()

    for monkey_id, line in enumerate(input_text.splitlines()):
        part2_monkey_sequence = deque[int]()
        # Create new dict
        part2_sequences[monkey_id] = {}

        number = int(line)
        part2_price = number % 10
        for _ in range(2000):
            part2_old_price = part2_price
            number = generate_new_secret(number)
            part2_price = number % 10

            # Update sequence
            part2_monkey_sequence.append(part2_price - part2_old_price)
            if 4 < len(part2_monkey_sequence):
                part2_monkey_sequence.popleft()

            # Skip if length of sequences is too short
            if len(part2_monkey_sequence) < 4:
                continue
            # Create entry of sequences
            sequence = tuple(part2_monkey_sequence)
            if sequence not in part2_sequences[monkey_id]:
                part2_sequences[monkey_id][sequence] = part2_price

        solution_part1.append(number)

    # Part 2 summing
    all_sequences = {
        sequence
        for monkey_sequence_dict in part2_sequences.values()
        for sequence in monkey_sequence_dict
    }
    sequences_total_sum = {
        sequence: sum(
            monkey_sequence_dict.get(sequence, 0)
            for monkey_sequence_dict in part2_sequences.values()
        )
        for sequence in all_sequences
    }

    answer_part1 = sum(solution_part1)
    answer_part2 = max(sequences_total_sum.values())
    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example = solve(
        """
1
10
100
2024
""".strip()
    )
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 37327623

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example = solve(input_example_text)
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 23

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
