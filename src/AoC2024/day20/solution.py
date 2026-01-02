import math


from heapq import heappop, heappush
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

type Vec = tuple[int, int]


def get_char(text_grid: list[str], pos: Vec) -> str:
    # Out of grid
    if not (0 <= pos[1] < len(text_grid)) or not (0 <= pos[0] < len(text_grid[0])):
        return ""
    return text_grid[pos[1]][pos[0]]


def add_vec(v1: Vec, v2: Vec) -> Vec:
    return v1[0] + v2[0], v1[1] + v2[1]


def solve(
    input_text: str, cheat_duration: int = 2, min_time_saved: int = 100
) -> tuple[int, int]:
    grid = input_text.splitlines()
    neighbors: list[Vec] = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    start = next(
        (
            (x, y)
            for y, row in enumerate(grid)
            for x, value in enumerate(row)
            if value == "S"
        ),
        None,
    )
    end = next(
        (
            (x, y)
            for y, row in enumerate(grid)
            for x, value in enumerate(row)
            if value == "E"
        ),
        None,
    )
    if start is None:
        return 0, 0
    if end is None:
        return 0, 0

    came_from_score = dict[Vec, int]()

    already_visited = set[Vec]()
    # position (Vec), cheat_activated_position (Vec)
    already_visited_cheat = set[tuple[Vec, Vec]]()
    # distance from start (int), pos (Vec)
    queue = list[tuple[int, int, int]]()
    # distance from start (int), pos (Vec), cheat_active (int), cheat used at pos (Vec)
    queue_cheat = list[tuple[int, int, int, int, Vec]]()

    # Distance to start, cheatsavailable
    path_length_without_cheat = -1
    paths = list[tuple[int, Vec | None]]()

    def iterate(cheat: bool, end_char: str = "E"):
        nonlocal path_length_without_cheat
        if not cheat:
            cheat_active = -1
            cheat_used_at_pos = (-1, -1)
            distance_to_start, pos_x, pos_y = heappop(queue)
        else:
            distance_to_start, pos_x, pos_y, cheat_active, cheat_used_at_pos = heappop(
                queue_cheat
            )
        pos = (pos_x, pos_y)

        char = get_char(grid, pos)

        # Already used this path
        if cheat and cheat_used_at_pos != (-1, -1) and pos in came_from_score:
            total_distance = came_from_score[pos] + distance_to_start
            if path_length_without_cheat < total_distance:
                return
            if cheat_active <= 0:
                paths.append((total_distance, cheat_used_at_pos))
                return
        # End reached
        if not cheat and char == end_char:
            path_length_without_cheat = distance_to_start
            return
        if cheat and char == end_char:
            paths.append((distance_to_start, cheat_used_at_pos))
            return

        if not cheat:
            already_visited.add(pos)
        else:
            already_visited_cheat.add((pos, cheat_used_at_pos))

        for neighbor in neighbors:
            new_pos = add_vec(pos, neighbor)

            if not cheat and new_pos in already_visited:
                continue
            if cheat and (new_pos, cheat_used_at_pos) in already_visited_cheat:
                continue

            char = get_char(grid, new_pos)
            if char in {".", end_char}:
                if not cheat:
                    heappush(queue, (distance_to_start + 1, *new_pos))
                    # Cache for cheat path: already seen this position, we know distance to end
                    if distance_to_start + 1 < came_from_score.get(new_pos, math.inf):
                        came_from_score[new_pos] = distance_to_start + 1
                else:
                    heappush(
                        queue_cheat,
                        (
                            distance_to_start + 1,
                            *new_pos,
                            max(0, cheat_active - 1),
                            cheat_used_at_pos,
                        ),
                    )
            # Go through wall
            if cheat and 1 < cheat_active and char == "#":
                heappush(
                    queue_cheat,
                    (
                        distance_to_start + 1,
                        *new_pos,
                        cheat_active - 1,
                        cheat_used_at_pos,
                    ),
                )
            # Activate cheat
            if cheat and cheat_used_at_pos == (-1, -1) and char == "#":
                heappush(
                    queue_cheat,
                    (distance_to_start + 1, *new_pos, cheat_duration - 1, pos),
                )

    # Build path from end to finish, for came_from_score
    heappush(queue, (0, *end))
    while queue and path_length_without_cheat == -1:
        iterate(cheat=False, end_char="S")

    heappush(queue_cheat, (0, *start, 0, (-1, -1)))
    while queue_cheat:
        iterate(cheat=True)

    path_that_save_time = sorted(
        [
            i
            for i in paths
            if i[0] <= path_length_without_cheat - min_time_saved and i[1] is not None
        ]
    )

    answer_part1 = len(path_that_save_time)

    answer_part2 = 0
    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example = solve(input_example_text, cheat_duration=2, min_time_saved=100)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 0

    solution = solve(input_text, cheat_duration=2, min_time_saved=100)
    answer_part1 = solution[0]  # 1381
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example = solve(input_example_text, cheat_duration=20, min_time_saved=50)
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 0

    solution = solve(input_text, cheat_duration=20, min_time_saved=50)
    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
