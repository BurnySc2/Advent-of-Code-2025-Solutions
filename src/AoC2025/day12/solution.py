# Currently does not solve part 1 or part 2
from dataclasses import dataclass
from pathlib import Path

import grilops
from grilops.geometry import Point, RectangularLattice, Vector
from grilops.shapes import Shape, ShapeConstrainer

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

type Grid = list[list[str]]
type MyShape = list[str]


@dataclass
class Region:
    width: int
    height: int
    shapes: list[int]


def parse(text: str) -> tuple[list[MyShape], list[Region]]:
    shapes: list[MyShape] = []
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


def part1_step(
    region: Region,
    shapes: list[MyShape],
    shapes_target: list[int],
) -> bool:
    points = [Point(y, x) for y in range(region.height) for x in range(region.width)]
    lattice = RectangularLattice(points)

    my_shapes: list[Shape[Vector]] = [  # pyright: ignore[reportInvalidTypeArguments]
        Shape(
            [
                Vector(y, x)
                for y in range(3)
                for x in range(3)
                if shapes[shape_index][y][x] == "#"
            ]
        )
        for shape_index, count in enumerate(shapes_target)
        for _ in range(count)
    ]

    sym = grilops.SymbolSet(["B", "W"])
    sg = grilops.SymbolGrid(lattice, sym)
    _sc = ShapeConstrainer(
        lattice,
        my_shapes,
        sg.solver,
        complete=False,
        allow_rotations=True,
        allow_reflections=True,
        allow_copies=False,
    )

    return bool(sg.solve())


def solve(input_text: str) -> tuple[int, int]:
    shapes, regions = parse(input_text)
    count_possible = 0
    for region in regions:
        # grid = [["." for _ in range(region.width)] for _ in range(region.height)]
        possible = part1_step(region, shapes, region.shapes)
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
