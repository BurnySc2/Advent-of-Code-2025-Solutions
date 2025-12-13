from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve_part1(numbers: list[int]) -> bool:
    last_number = None
    all_increasing = True
    all_decreasing = True
    for i in numbers:
        if last_number is None:
            last_number = i
            continue
        if not (0 < abs(i - last_number) <= 3):
            all_increasing = False
            all_decreasing = False
            break
        if i > last_number:
            all_decreasing = False
        if i < last_number:
            all_increasing = False
        last_number = i
    return all_increasing or all_decreasing


def solve(input_text: str) -> tuple[int, int]:
    numbers_rows: list[list[int]] = []
    for line in input_text.splitlines():
        numbers_rows.append(list(map(int, line.split())))

    part1_solution = 0
    for numbers in numbers_rows:
        if solve_part1(numbers):
            part1_solution += 1

    part2_solution = 0
    for numbers in numbers_rows:
        for index, _ in enumerate(numbers):
            if solve_part1(numbers[:index] + numbers[index + 1 :]):
                part2_solution += 1
                break

    return part1_solution, part2_solution


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 2

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 4

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
