from itertools import product
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve(input_text: str) -> tuple[int, int]:
    locks = list[list[str]]()
    keys = list[list[str]]()

    for part in input_text.split("\n\n"):
        part = part.splitlines()
        if set(part[0]) == {"#"}:
            locks.append(part)
        else:
            keys.append(part)

    def get_height(part: list[str]) -> list[int]:
        heights = [
            sum(1 if part[y][x] == "#" else 0 for y, _ in enumerate(part)) - 1
            for x, _ in enumerate(part[0])
        ]
        return heights

    lock_heights = list(map(get_height, locks))
    key_heights = list(map(get_height, keys))
    max_height_sum = len(locks[0]) - 2

    answer_part1 = 0
    for lock, key in product(lock_heights, key_heights):
        no_overlap = True
        for lock_height, key_height in zip(lock, key):
            if max_height_sum < lock_height + key_height:
                no_overlap = False
                break
        if no_overlap:
            answer_part1 += 1

    return answer_part1, 0


def main():
    # Part 1
    solution_example = solve(input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 3

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    # TODO Part 2
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 11387

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
