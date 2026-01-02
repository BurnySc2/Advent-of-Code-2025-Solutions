from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

# Opcode, Operand
type Instruction = tuple[int, int]


def solve(input_text: str) -> tuple[str, int]:
    input_list = input_text.splitlines()
    register_a = int(input_list[0].split(":")[1])
    register_b = int(input_list[1].split(":")[1])
    register_c = int(input_list[2].split(":")[1])
    instructions_list = input_list[4].split(":")[1].split(",")
    # instructions: list[Instruction] = []
    # for i in range(0, len(insturctions_list), 2):
    #     instructions.append((int(insturctions_list[i]), int(insturctions_list[i + 1])))

    instruction_pointer = 0
    out_values = list[int]()
    while instruction_pointer < len(instructions_list):
        opcode, operand = list(
            map(
                int,
                [
                    instructions_list[instruction_pointer],
                    instructions_list[instruction_pointer + 1],
                ],
            )
        )

        assert operand in range(7)
        if 0 <= operand <= 3:
            value = operand
        elif operand == 4:
            value = register_a
        elif operand == 5:
            value = register_b
        elif operand == 6:
            value = register_c

        if opcode == 0:
            register_a = register_a >> value  # pyright: ignore[reportPossiblyUnboundVariable]
        if opcode == 1:
            register_b = register_b ^ operand
        if opcode == 2:
            register_b = value % 8  # pyright: ignore[reportPossiblyUnboundVariable]
        if opcode == 3:
            if register_a != 0:
                instruction_pointer = operand
                continue
        if opcode == 4:
            register_b = register_b ^ register_c
        if opcode == 5:
            out_values.append(value % 8)  # pyright: ignore[reportPossiblyUnboundVariable]
        if opcode == 6:
            register_b = register_a >> value  # pyright: ignore[reportPossiblyUnboundVariable]
        if opcode == 7:
            register_c = register_a >> value  # pyright: ignore[reportPossiblyUnboundVariable]
        instruction_pointer += 2

    answer_part1 = ",".join(map(str, out_values))
    return answer_part1, 0


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == "4,6,3,5,6,3,5,2,1,0"

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    # TODO Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 11387

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
