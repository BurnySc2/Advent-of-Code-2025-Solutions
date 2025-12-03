from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def get_maximum_2(line: str) -> int:
    """
    From input "98765432111" find the maximum possible number using only two numbers, here: 98
    """
    index1 = 0
    index2 = 1
    for index, char in enumerate(line[2:], start=2):
        if int(line[index1]) < int(line[index2]):
            index1 = index2
            index2 = index
        elif int(line[index2]) < int(char):
            index2 = index
    result = 10 * int(line[index1]) + int(line[index2])
    return result


def get_maximum_12(line: str) -> int:
    """
    From input "987654321101" find the maximum possible number using only two numbers, here: 98
    """
    indices = list(range(12))
    for char_index, char in enumerate(line[12:], start=12):
        for list_index1, _list_char in enumerate(indices):
            # At last index: compare value and override
            if list_index1 == 11:
                if indices[list_index1] == -1:
                    indices[list_index1] = char_index
                elif int(line[indices[list_index1]]) < int(char):
                    indices[list_index1] = char_index
                continue

            list_index2 = list_index1 + 1
            if indices[list_index1] == -1:
                # Index is set to -1, shift!
                indices[list_index1] = indices[list_index2]
                indices[list_index2] = -1
                continue

            if int(line[indices[list_index1]]) < int(line[indices[list_index2]]):
                # Number at index is smaller than at next index, shift!
                indices[list_index1] = indices[list_index2]
                indices[list_index2] = -1

    result_list: list[int] = [
        10**index * int(line[i]) for index, i in enumerate(indices[::-1])
    ]
    result = sum(result_list)
    return result


def solve(input_text: str) -> tuple[int, int]:
    result_sum_part1 = 0
    result_sum_part2 = 0
    for line in input_text.split("\n"):
        if line.strip() == "":
            continue
        line_sum_part1 = get_maximum_2(line.strip())
        result_sum_part1 += line_sum_part1
        line_sum_part2 = get_maximum_12(line.strip())
        result_sum_part2 += line_sum_part2
    return result_sum_part1, result_sum_part2


def main():
    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 357

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 3121910778619

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
