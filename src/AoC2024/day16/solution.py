import heapq
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

# x, y
type Vec = tuple[int, int]


def get_char(text_grid: list[str], pos: Vec) -> str:
    # Out of grid
    if not (0 <= pos[1] < len(text_grid)) or not (0 <= pos[0] < len(text_grid[0])):
        return ""
    return text_grid[pos[1]][pos[0]]


def add_vec(v1: Vec, v2: Vec) -> Vec:
    return v1[0] + v2[0], v1[1] + v2[1]


def solve(input_text: str) -> tuple[int, int]:
    grid = input_text.splitlines()
    neighbors: list[Vec] = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    # total_score, x, y, dir_x, dir_y, debug_steps, debug_rotations
    queue = list[tuple[int, list[Vec], int, int, int, int, int, int]]()
    visited = dict[tuple[int, int, int, int], int]()

    start = next(
        (x, y)
        for y, row in enumerate(grid)
        for x, value in enumerate(row)
        if value == "S"
    )
    goal = next(
        (x, y)
        for y, row in enumerate(grid)
        for x, value in enumerate(row)
        if value == "E"
    )

    # Part 1
    heapq.heappush(queue, (0, [], *start, 1, 0, 0, 0))
    paths = list[int]()
    paths_with_positions = list[tuple[int, list[Vec]]]()

    def iterate(
        score: int,
        visited_positions: list[Vec],
        current_location: Vec,
        current_rotation: Vec,
        debug_steps: int,
        debug_rotations: int,
    ):
        if current_location == goal:
            paths.append(score)
            paths_with_positions.append((score, visited_positions))
            return

        # Optional
        # if visited.get((*current_location, *current_rotation), math.inf) < score:
        #     return

        visited[(*current_location, *current_rotation)] = score

        for neighbor in neighbors:
            new_pos = add_vec(current_location, neighbor)
            # Already visited, don't run in circles
            if (*new_pos, *neighbor) in visited:
                continue
            char = get_char(grid, new_pos)
            # Wall check
            if char in {"", "#"}:
                continue

            new_score = score + 1
            new_debug_steps = debug_steps + 1
            new_debug_rotations = debug_rotations
            if neighbor != current_rotation:
                new_score += 1000
                new_debug_rotations += 1
            new_visited_positions = visited_positions + [new_pos]
            heapq.heappush(
                queue,
                (
                    new_score,
                    new_visited_positions,
                    *new_pos,
                    *neighbor,
                    new_debug_steps,
                    new_debug_rotations,
                ),
            )

    answer_part1 = 0
    while queue:
        score, visited_positions, x, y, dir_x, dir_y, debug_steps, debug_rotations = (
            heapq.heappop(queue)
        )
        iterate(
            score,
            visited_positions,
            (x, y),
            (dir_x, dir_y),
            debug_steps,
            debug_rotations,
        )
    answer_part1 = min(paths)

    part2_best_path = min(paths_with_positions)[0]
    positions = {
        pos
        for path in paths_with_positions
        for pos in path[1]
        if path[0] == part2_best_path
    }
    answer_part2 = len(positions) + 1

    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 7036

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 45

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
