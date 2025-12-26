from operator import and_, or_, xor
from pathlib import Path
import re
from typing import Callable


input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve(input_text: str) -> tuple[int, int]:
    # name: 0|1
    # or
    # name: (operand1, operador, operand2)
    rules = dict[str, int | tuple[str, str, str]]()
    for line in input_text.splitlines():
        match1 = re.fullmatch(r"(\w+): (\d)", line)
        match2 = re.fullmatch(r"(\w+) (XOR|OR|AND) (\w+) -> (\w+)", line)
        if match1:
            name, value = match1.groups()
            rules[name] = int(value)
        if match2:
            operand1, operator, operand2, name = match2.groups()
            rules[name] = operand1, operator, operand2

    def evaluate(name: str) -> int:
        value = rules[name]
        if isinstance(value, int):
            return value
        operators = {
            "XOR": xor,
            "AND": and_,
            "OR": or_,
        }
        operand1, operator_, operand2 = value
        operator_: Callable[[int, int], int] = operators[operator_]  # pyright: ignore[reportArgumentType]
        operand1 = evaluate(operand1)
        operand2 = evaluate(operand2)
        return operator_(operand1, operand2)

    binary_values = [
        evaluate(name) for name in sorted(rules, reverse=True) if name.startswith("z")
    ]
    answer_part1 = int("".join(map(str, binary_values)), 2)
    return answer_part1, 0


def main():
    # Part 1
    solution_example = solve(input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 2024

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
