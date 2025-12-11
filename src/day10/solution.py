from dataclasses import dataclass
import math
from pathlib import Path
from typing import Literal
from itertools import product
import math
from sympy import symbols, Matrix, linsolve
from sympy import Tuple

from loguru import logger

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


@dataclass
class MyInput:
    target: list[Literal[".", "#"]]
    buttons: list[list[int]]
    joltage_requirements: list[int]


def parse_line(text: str) -> MyInput:
    target_str, rest = text.split("]")
    target = list(target_str.strip("["))

    rest, joltage_str = rest.split("{")
    joltage = list(map(int, joltage_str.strip("}").split(",")))

    buttons_str = rest.strip()
    buttons: list[list[int]] = []
    for button_combo in buttons_str.split(" "):
        buttons_combo = [i.strip("()") for i in button_combo.split(",")]
        buttons.append([int(i) for i in buttons_combo])

    return MyInput(
        target=target,  # pyright: ignore[reportArgumentType]
        buttons=buttons,
        joltage_requirements=joltage,
    )


def part1_get_state_from_buttons(
    target: list[Literal[".", "#"]], buttons: list[list[int]], button_states: list[int]
) -> list[Literal[".", "#"]]:
    assert len(buttons) == len(button_states)
    result_list: list[int] = [0 for _ in target]
    for button, enabled in zip(buttons, button_states):
        assert enabled in {0, 1}
        if enabled == 0:
            continue
        for number in button:
            result_list[number] += 1
    return ["#" if i % 2 == 1 else "." for i in result_list]


def solve_part1(parsed: list[MyInput]) -> int:
    best_sum_part1 = 0
    for my_input in parsed:
        current_best: int = math.inf  # pyright: ignore[reportAssignmentType]

        length = len(my_input.buttons)
        for combo in range(2**length, 2 ** (length + 1)):
            binary = bin(combo)[3:]
            count_button_presses = binary.count("1")
            if current_best < count_button_presses:
                # Early continue
                continue

            button_states = list(map(int, binary))
            estimated_end_state = part1_get_state_from_buttons(
                my_input.target, my_input.buttons, button_states
            )
            if my_input.target == estimated_end_state:
                current_best = count_button_presses
        best_sum_part1 += current_best
    return best_sum_part1


# TODO Try different limit values
def part2_task_solver(
    numbers: list[list[int]],
    b_vector: list[int],
    limit: int = 50,
) -> int:
    b_vec = Matrix(b_vector)

    A = Matrix([[0 for _ in range(len(numbers))] for _ in range(len(b_vec))])
    for x, numbers_array in enumerate(numbers):
        for y in range(len(b_vec)):
            if y in numbers_array:
                A[y, x] = 1

    solution_set: list[Tuple] = linsolve((A, b_vec))  # pyright: ignore[reportAssignmentType]

    best_result: int = math.inf  # pyright: ignore[reportAssignmentType]
    # general_solution: Tuple = list(solution_set)[0]
    for solution in solution_set:
        vars_list: list[str] = sorted(solution.free_symbols, key=lambda s: s.name)  # pyright: ignore[reportUnknownLambdaType, reportAttributeAccessIssue, reportUnknownMemberType, reportAssignmentType]

        for values in product(range(limit), repeat=len(vars_list)):
            assignment = dict(zip(vars_list, values))
            # Now you can substitute into the expressions:
            substituted: list[int] = solution.subs(assignment)  # pyright: ignore[reportUnknownMemberType, reportAssignmentType]

            # A coefficient reached a value smaller than 0
            if any(i < 0 for i in substituted):
                continue
            # A coefficient reached a value of a fraction
            if any(i != int(i) for i in substituted):
                continue

            current_sum_coefficients = sum(substituted)
            if current_sum_coefficients < best_result:
                best_result = current_sum_coefficients
    if best_result == math.inf:
        return part2_task_solver(numbers, b_vector, limit * 2)
    return best_result


def solve_part2(parsed: list[MyInput]) -> int:
    best_sum_part2 = 0
    for i, my_input in enumerate(parsed):
        solution = part2_task_solver(my_input.buttons, my_input.joltage_requirements)
        logger.info(f"{i + 1} / {len(parsed)}")
        best_sum_part2 += solution

    return best_sum_part2


def solve(input_text: str) -> tuple[int, int]:
    parsed = [parse_line(line) for line in input_text.split("\n") if line.strip()]
    # Sanity check
    for my_input in parsed:
        assert 0 < len(my_input.target)
        assert 0 < len(my_input.buttons)
        for button in my_input.buttons:
            assert 0 < len(button)

    return solve_part1(parsed), solve_part2(parsed)


def main():
    # Sanity check
    example_line = """[....#..#.#] (1,4) (2,8) (0,1,2,4,5,7,8,9) (2,3) (1,2,4,5,6,7,8,9) (2,5) (0,4,8,9) (1,3,4,5,6,7,8,9) (0,2,4,9) (0,1) (1,3,7) {23,54,52,41,58,39,28,43,65,49}"""
    parsed = solve(example_line)
    assert parsed[0] == 4

    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 7

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 33

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
