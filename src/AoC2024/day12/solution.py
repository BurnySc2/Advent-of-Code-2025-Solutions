from pathlib import Path
from typing import Literal

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

# x, y
type Vec = tuple[int, int]
# x, y, position
type Fence = tuple[int, int, Literal["below", "above", "left", "right"]]


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
    neighbor_names: list[Literal["below", "above", "left", "right"]] = [
        "below",
        "above",
        "left",
        "right",
    ]

    already_visited: set[Vec] = set()
    plant_locations: set[Vec] = set()
    fence_locations: set[Fence] = set()

    def dfs(current_position: Vec, plant_name: str) -> None:
        if current_position in already_visited:
            return

        char = get_char(grid, current_position)
        if char != plant_name:
            return

        already_visited.add(current_position)
        plant_locations.add(current_position)

        for neighbor, neighbor_name in zip(neighbors, neighbor_names):
            new_pos = add_vec(current_position, neighbor)

            fence_locations.add((*new_pos, neighbor_name))

            dfs(new_pos, plant_name)

    answer_part1 = 0
    answer_part2 = 0

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            # Reset count
            plant_locations = set()
            fence_locations = set()
            # Check region and perimeter
            dfs((x, y), value)
            # Location already checked?z
            if len(plant_locations) == 0:
                continue
            region_size = len(plant_locations)
            perimeter_size = 0
            for pos in fence_locations:
                if (pos[0], pos[1]) in plant_locations:
                    continue
                perimeter_size += 1
            answer_part1 += region_size * perimeter_size

            sides_count = 0
            # Check all vertical fences, ordered by x-value then y-value
            previous_fence = None
            for vertical_fence in sorted(
                fence_locations, key=lambda i: (i[2], i[0], i[1])
            ):
                # Skip same as plant locaton
                if (vertical_fence[0], vertical_fence[1]) in plant_locations:
                    continue
                # Only checking vertical fences here
                if vertical_fence[2] in ["below", "above"]:
                    continue
                if previous_fence is None or previous_fence[2] != vertical_fence[2]:
                    # New side
                    sides_count += 1
                elif (
                    previous_fence[0] != vertical_fence[0]
                    or previous_fence[1] + 1 != vertical_fence[1]
                ):
                    # New side, not directly below
                    sides_count += 1
                previous_fence = vertical_fence
            for horizontal_fence in sorted(
                fence_locations, key=lambda i: (i[2], i[1], i[0])
            ):
                # Skip same as plant locaton
                if (horizontal_fence[0], horizontal_fence[1]) in plant_locations:
                    continue
                # Only checking horizontal fences here
                if horizontal_fence[2] in ["left", "right"]:
                    continue
                if previous_fence is None or previous_fence[2] != horizontal_fence[2]:
                    # New side
                    sides_count += 1
                elif (
                    previous_fence[0] + 1 != horizontal_fence[0]
                    or previous_fence[1] != horizontal_fence[1]
                ):
                    # New side, not directly to the right
                    sides_count += 1
                previous_fence = horizontal_fence
            answer_part2 += region_size * sides_count

    return answer_part1, answer_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 1930

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 1206

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
