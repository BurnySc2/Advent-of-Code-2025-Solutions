# Currently does not solve part 1 or part 2
from dataclasses import dataclass
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

type Shape = list[str]
type Grid = list[list[str]]


@dataclass
class Region:
    width: int
    height: int
    shapes: list[int]


def parse(text: str) -> tuple[list[Shape], list[Region]]:
    shapes: list[Shape] = []
    regions: list[Region] = []

    current_shape: list[str] = []
    for line in text.splitlines():
        if line.endswith(":"):
            continue
        if line.strip() == "" and current_shape != []:
            shapes.append(current_shape)
            current_shape = []
            continue

        if len(shapes) < 6:
            current_shape.append(line)
        else:
            dims, *shape_values = line.split(" ")
            regions.append(
                Region(
                    width=int(dims.split("x")[0]),
                    height=int(dims.split("x")[1].strip(":")),
                    shapes=[int(i) for i in shape_values],
                )
            )
    return shapes, regions


def rotate_shape(shape: Shape, amount: int) -> Shape:
    if amount == 0:
        return shape
    assert 0 < amount < 4
    if amount == 1:
        return [
            "".join(shape[len(shape[0]) - y - 1][x] for y, _ in enumerate(shape))
            for x, _ in enumerate(shape[0])
        ]
    if amount == 2:
        return [shape[-i][::-1] for i, _ in enumerate(shape, start=1)]
    if amount == 3:
        return [
            "".join(shape[y][-x] for y, _ in enumerate(shape))
            for x, _ in enumerate(shape[0], start=1)
        ]
    return []


assert rotate_shape(
    ["...", "..#", "..."],
    1,
) == ["...", "...", ".#."]
assert rotate_shape(
    ["...", "..#", "..."],
    2,
) == ["...", "#..", "..."]
assert rotate_shape(
    ["...", "..#", "..."],
    3,
) == [".#.", "...", "..."]


def mirror_shape(shape: Shape, mirror_axis: int) -> Shape:
    if mirror_axis == -1:
        return shape
    assert mirror_axis in [0, 1]
    if mirror_axis == 0:
        return [i[::-1] for i in shape]
    if mirror_axis == 1:
        return [shape[-i] for i, _ in enumerate(shape, start=1)]
    return []


assert mirror_shape(
    ["...", "..#", "..."],
    0,
) == ["...", "#..", "..."]
assert mirror_shape(
    ["...", "..#", ".#."],
    1,
) == [".#.", "..#", "..."]


def can_place_shape(current_region: Grid, shape: Shape, pos: tuple[int, int]) -> bool:
    # All shapes are 3x3
    assert len(shape) == 3
    assert len(shape[0]) == 3
    y, x = pos
    for offset_y in range(3):
        for offset_x in range(3):
            if (
                current_region[y + offset_y][x + offset_x] == "#"
                and shape[offset_y][offset_x] == "#"
            ):
                return False
    return True


def insert_shape_into_grid(
    current_region: Grid, shape: Shape, pos: tuple[int, int]
) -> Grid:
    # Create copy
    new_grid = [list(row) for row in current_region]
    y, x = pos
    for offset_y in range(3):
        for offset_x in range(3):
            if shape[offset_y][offset_x] == "#":
                new_grid[y + offset_y][x + offset_x] = "#"
    return new_grid


def part1_step(
    region: Grid,
    shapes: list[Shape],
    shapes_placed: list[int],
    target_shapes_placed: list[int],
    current_shape_index: int,
    pos: tuple[int, int],
) -> bool:
    # Abort condition
    if shapes_placed == target_shapes_placed:
        return True
    if len(shapes) <= current_shape_index:
        return False
    if len(region) - 2 <= pos[0]:
        return False
    if len(region[0]) - 2 <= pos[1]:
        return False

    new_grid = None
    shapes_placed_copy = None
    inserted = False
    # Enough shapes of that kind placed?
    if shapes_placed[current_shape_index] < target_shapes_placed[current_shape_index]:
        for mirror in range(-1, 2):
            for rotation in range(0, 4):
                if inserted:
                    break
                rotated = rotate_shape(
                    mirror_shape(shapes[current_shape_index], mirror), rotation
                )
                if can_place_shape(region, rotated, pos):
                    new_grid = insert_shape_into_grid(region, rotated, pos)
                    shapes_placed_copy = list(shapes_placed)
                    shapes_placed_copy[current_shape_index] += 1
                    inserted = True
    return (
        part1_step(
            new_grid or region,
            shapes,
            shapes_placed_copy or shapes_placed,
            target_shapes_placed,
            current_shape_index + 1,
            pos,
        )
        or part1_step(
            new_grid or region,
            shapes,
            shapes_placed_copy or shapes_placed,
            target_shapes_placed,
            0,
            (pos[0] + 1, pos[1]),
        )
        or part1_step(
            new_grid or region,
            shapes,
            shapes_placed_copy or shapes_placed,
            target_shapes_placed,
            0,
            (0, pos[1] + 1),
        )
    )


def solve(input_text: str) -> tuple[int, int]:
    shapes, regions = parse(input_text)
    count_possible = 0
    for region in regions:
        grid = [["." for _ in range(region.width)] for _ in range(region.height)]
        possible = part1_step(
            grid, shapes, [0 for _ in shapes], region.shapes, 0, (0, 0)
        )
        if possible:
            count_possible += 1
    return count_possible, 0


def main():
    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 2

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    # answer_example_part2 = solution_example[1]
    # print(f"The solution for the example for part2 is: {answer_example_part2=}")
    # assert answer_example_part2 == 40

    # answer_part2 = solution[1]
    # print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
