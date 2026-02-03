from collections.abc import Callable
from pathlib import Path
import re
from typing import Literal
from loguru import logger
from pydantic import BaseModel
from operator import gt, lt

input_example_p1_path = Path(__file__).parent / "example_input_p1.txt"
input_example_p1_text = input_example_p1_path.read_text()
input_example_p2_path = Path(__file__).parent / "example_input_p2.txt"
input_example_p2_text = input_example_p2_path.read_text()
input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()


class Category(BaseModel):
    x: int
    m: int
    a: int
    s: int


class Rule(BaseModel):
    operand: str
    operator: Literal[">", "<"]
    value: int
    target: str


ops: dict[str, Callable[[int, int], bool]] = {
    "<": lt,
    ">": gt,
}


def build_rules_dict(lines: list[str]):
    tree = dict[str, list[str | Rule]]()
    for line in lines:
        line = line.strip("}")
        name, rest = line.split("{")

        rules = list[str | Rule]()
        for rule in rest.split(","):
            if ":" not in rule:
                rules.append(rule)
                continue
            operand = rule[0]
            operator = rule[1]
            value, target = rule[2:].split(":")
            rules.append(
                Rule(
                    operand=operand,
                    operator=operator,
                    value=int(value),
                    target=target,
                )
            )
        tree[name] = rules
    return tree


def solve(input_text: str) -> tuple[int, int]:
    answer_part1 = answer_part2 = 0
    upper, lower = input_text.split("\n\n")

    rules = build_rules_dict(upper.split("\n"))

    for start_value in lower.split("\n"):
        x, m, a, s = map(
            int,
            re.fullmatch(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", start_value).groups(),
        )
        category = Category(x=x, m=m, a=a, s=s)
        current_value = "in"
        while current_value not in ["A", "R"]:
            for rule in rules[current_value]:
                match rule:
                    case str(v):
                        current_value = v
                        break
                    case Rule(
                        operand=operand,
                        operator=operator,
                        value=value,
                        target=target,
                    ):
                        category_value: int = category.__dict__[operand]
                        is_match = ops[operator](category_value, value)
                        if is_match:
                            current_value = target
                            break
        if current_value == "A":
            my_sum = sum([x, m, a, s])
            answer_part1 += my_sum

    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_p1 = solve(input_example_p1_text)
    answer_example_part1 = solution_example_p1[0]
    logger.info(f"The solution for the example for part1 is: {answer_example_part1 = }")
    assert answer_example_part1 == 19114

    # Part 2
    solution_example_p2 = solve(input_example_p2_text)
    answer_example_part2 = solution_example_p2[1]
    logger.info(f"The solution for the example for part2 is: {answer_example_part2 = }")
    assert answer_example_part2 == 167409079868000

    solution = solve(input_text)
    answer_part1 = solution[0]
    logger.info(f"The solution for the part1 is: {answer_part1 = }")
    answer_part2 = solution[1]
    logger.info(f"The solution for the part2 is: {answer_part2 = }")


if __name__ == "__main__":
    main()
