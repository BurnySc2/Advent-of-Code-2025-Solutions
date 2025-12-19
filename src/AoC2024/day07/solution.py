from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def apply_operator(num1: int, num2: int, operator: str) -> int:
    if operator == "+":
        return num1 + num2
    if operator == "*":
        return num1 * num2
    # || case
    return int(f"{num1}{num2}")


def check_possible(
    numbers: tuple[int, ...],
    target_value: int,
    allow_part2_operator: bool = False,
) -> bool:
    if not numbers:
        return target_value != 0

    available_signs = "+*|" if allow_part2_operator else "+*"

    def dfs(index: int, current_value: int) -> bool:
        nonlocal available_signs, numbers, target_value

        if target_value < current_value:
            return False

        if len(numbers) == index:
            return target_value == current_value

        return any(
            dfs(index + 1, apply_operator(current_value, numbers[index], sign))
            for sign in available_signs
        )

    return dfs(1, numbers[0])


def solve(input_text: str) -> tuple[int, int]:
    problems: list[tuple[int, tuple[int, ...]]] = []
    for line in input_text.splitlines():
        target, *numbers = line.split(" ")
        target = int(target.strip(":"))
        numbers = tuple(map(int, numbers))
        problems.append((target, numbers))

    solution_part1 = sum(
        target for target, numbers in problems if check_possible(numbers, target)
    )
    solution_part2 = sum(
        target for target, numbers in problems if check_possible(numbers, target, True)
    )

    return solution_part1, solution_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 3749

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 11387

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
