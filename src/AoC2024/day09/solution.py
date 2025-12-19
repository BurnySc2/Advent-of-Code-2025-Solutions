from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def calculate_checksum(data: list[int]) -> int:
    checksum = 0
    for index, number in enumerate(data):
        if number == -1:
            continue
        checksum += index * number
    return checksum


def solve_part1(data: list[int]) -> int:
    left_index = 0
    right_index = len(data) - 1
    while left_index < right_index:
        # Find a gap
        if data[left_index] != -1:
            left_index += 1
            continue
        # Find a number
        if data[right_index] == -1:
            right_index -= 1
            continue

        # Swap
        data[left_index] = data[right_index]
        data[right_index] = -1

        # Move to the middle
        left_index, right_index = left_index + 1, right_index - 1

    return calculate_checksum(data)


def solve_part2(data: list[int], input_text: str) -> int:
    # start_index, space
    gaps: list[tuple[int, int]] = []

    current_index = 0
    to_add = False
    for char in input_text:
        if to_add:
            gaps.append((current_index, int(char)))
        current_index += int(char)
        to_add = not to_add

    window_left = len(data) - 1
    window_right = len(data) - 1
    while 0 < window_right:
        data_changed = False

        # Move sliding window to match max possible size
        if data[window_right] == -1:
            window_right -= 1
            window_left = window_right
            continue
        if data[window_left - 1] == data[window_right]:
            window_left -= 1
            continue

        # print("".join(map(str, [i if i >= 0 else "." for i in data])))

        # Try to find gap to swap
        window_size = window_right - window_left + 1
        for gaps_index, (gap_index, gap_size) in enumerate(gaps[:]):
            if window_right < gap_index:
                break

            if window_size <= gap_size:
                data_changed = True

                # Execute swap
                value = data[window_right]
                data[gap_index : gap_index + window_size] = [
                    value for _ in range(window_size)
                ]

                # Set right side to -1
                data[window_left : window_right + 1] = [-1 for _ in range(window_size)]

                # Reduce gap_size
                if window_size < gap_size:
                    gaps[gaps_index] = gap_index + window_size, gap_size - window_size
                # Remove gap
                else:
                    gaps.pop(gaps_index)
                break

        if not data_changed:
            # Unable to find a gap, try next number
            window_right = window_left - 1
            window_left = window_right

    return calculate_checksum(data)


def solve(input_text: str) -> tuple[int, int]:
    data: list[int] = []

    is_data = True
    current_number = 0
    for i in input_text:
        if is_data:
            data.extend([current_number for _ in range(int(i))])
            current_number += 1
        else:
            data.extend([-1 for _ in range(int(i))])
        is_data = not is_data

    return solve_part1(data[:]), solve_part2(data[:], input_text)


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 1928

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 2858

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
