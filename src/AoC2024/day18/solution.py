import heapq
import math
from collections.abc import Sequence
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

# x, y
type Vec = tuple[int, int]


def get_char[T](text_grid: Sequence[Sequence[T]], pos: Vec) -> T | None:
    # Out of grid
    if not (0 <= pos[1] < len(text_grid)) or not (0 <= pos[0] < len(text_grid[0])):
        return None
    return text_grid[pos[1]][pos[0]]


def add_vec(v1: Vec, v2: Vec) -> Vec:
    return v1[0] + v2[0], v1[1] + v2[1]


def solve_part1(width: int, height: int, stones: list[Vec], count: int) -> int:
    grid = [["." for _ in range(width)] for _ in range(height)]
    for i, stone in enumerate(stones):
        if i == count:
            break
        grid[stone[1]][stone[0]] = "#"

    neighbors: list[Vec] = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    # total_score, x, y
    queue = list[tuple[int, int, int]]()
    already_seen = dict[tuple[int, int], int]()

    start = 0, 0
    goal = len(grid[0]) - 1, len(grid) - 1
    heapq.heappush(queue, (0, *start))
    paths = list[int]()

    def iterate(
        score: int,
        current_location: Vec,
    ):
        if current_location == goal:
            paths.append(score)
            return
        if already_seen.get(current_location, math.inf) <= score:
            return

        already_seen[current_location] = score

        for neighbor in neighbors:
            new_pos = add_vec(current_location, neighbor)
            # Already visited, don't run in circles
            if new_pos in already_seen:
                continue
            char = get_char(grid, new_pos)
            # Wall check
            if char in {None, "#"}:
                continue

            new_score = score + 1
            heapq.heappush(
                queue,
                (new_score, *new_pos),
            )

    answer_part1 = 0
    while queue:
        score, x, y = heapq.heappop(queue)
        iterate(score, (x, y))
        if 0 < len(paths):
            return min(paths)
    answer_part1 = min(paths, default=-1)
    return answer_part1


def solve_part2(width: int, height: int, stones: list[Vec]) -> str:
    for count, stone in enumerate(stones, start=1):
        answer_part2 = solve_part1(width, height, stones, count)
        if answer_part2 == -1:
            return f"{stone[0]},{stone[1]}"
    return ""


def solve(input_text: str, count: int = -1) -> tuple[int, str]:
    stones = list[Vec]()
    for line in input_text.splitlines():
        x, y = line.split(",")
        stones.append((int(x), int(y)))
    width = max(stones, key=lambda i: i[0])[0] + 1
    height = max(stones, key=lambda i: i[1])[1] + 1
    answer_part1 = solve_part1(width, height, stones, count)
    # Skip if calculating part1 only
    answer_part2 = ""
    if count == -1:
        answer_part2 = solve_part2(width, height, stones)
    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text, count=12)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 22

    solution = solve(input_text, count=1024)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == "6,1"

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
