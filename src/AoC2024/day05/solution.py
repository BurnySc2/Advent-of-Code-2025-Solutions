from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def correct_order(rules: list[tuple[int, int]], order: list[int]) -> bool:
    numbers_seen: set[int] = set()
    for number in order:
        for num1, num2 in rules:
            if number == num1 and num2 in numbers_seen:
                return False
        numbers_seen.add(number)
    return True


def solve_part1(rules: list[tuple[int, int]], orders: list[list[int]]) -> int:
    count = 0
    for order in orders:
        if correct_order(rules, order):
            count += order[len(order) // 2]
    return count


def solve_part2(rules: list[tuple[int, int]], orders: list[list[int]]) -> int:
    count = 0
    for order in orders:
        if correct_order(rules, order):
            # ALready ordered, don't add to result
            continue
        my_result: list[int] = []
        used_numbers: set[int] = set()
        while 1:
            blocked_numbers = {
                rule[0]
                for rule in rules
                if rule[1] not in used_numbers and rule[1] in order
            }
            for number in order:
                # Number not available or already used
                if number in blocked_numbers or number in used_numbers:
                    continue
                my_result.append(number)
                used_numbers.add(number)
            if len(my_result) == len(order):
                break
        count += my_result[len(my_result) // 2]
    return count


def solve(input_text: str) -> tuple[int, int]:
    rules: list[tuple[int, int]] = []
    orders: list[list[int]] = []
    rules_done = False
    for line in input_text.splitlines():
        if line.strip() == "":
            rules_done = True
            continue
        if not rules_done:
            i = line.split("|")
            rules.append((int(i[0]), int(i[1])))
        else:
            orders.append(list(map(int, line.split(","))))

    answer_part1 = solve_part1(rules, orders)
    answer_part2 = solve_part2(rules, orders)
    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 143

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 123

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
