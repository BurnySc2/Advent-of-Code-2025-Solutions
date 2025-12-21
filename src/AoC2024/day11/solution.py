from functools import cache
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve(input_text: str, problem_count: int) -> tuple[int, int]:
    initial: list[int] = list(map(int, input_text.split(" ")))

    @cache
    def dfs(number: int, count: int) -> int:
        if count == 0:
            return 1

        if number == 0:
            return dfs(1, count - 1)
        elif number == 1:
            return dfs(2024, count - 1)
        elif len(str(number)) % 2 == 0:
            number_str = str(number)
            first_half = int(number_str[: len(number_str) // 2])
            second_half = int(number_str[len(number_str) // 2 :])
            return dfs(first_half, count - 1) + dfs(second_half, count - 1)
        else:
            return dfs(number * 2024, count - 1)

    answer_part1 = sum(dfs(number, problem_count) for number in initial)

    return answer_part1, 0


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text, 25)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 55312

    solution = solve(input_text, 25)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    # solution_example_part2 = solve(input_example_text)
    # answer_example_part2 = solution_example_part2[1]
    # print(f"The solution for the example for part2 is: {answer_example_part2=}")
    # assert answer_example_part2 == 81

    solution_part2 = solve(input_text, 75)
    answer_part2 = solution_part2[0]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
