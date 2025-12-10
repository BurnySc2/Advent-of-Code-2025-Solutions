from dataclasses import dataclass
import math
from pathlib import Path

from loguru import logger

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def solve_part1(coords: list[tuple[int, int]]) -> int:
    max_value = 0
    for i, coord1 in enumerate(coords):
        for coord2 in coords[i + 1 :]:
            area = abs((coord1[0] - coord2[0] + 1) * (coord1[1] - coord2[1] + 1))
            if max_value < area:
                max_value = area
    return max_value


def distance(vec1: tuple[int, int], vec2: tuple[int, int]) -> float:
    return math.dist(vec1, vec2)


@dataclass
class MyRect:
    x: int
    y: int
    width: int
    height: int


def point_in_polygon(points: list[tuple[int, int]], point: tuple[int, int]) -> bool:
    # https://gist.github.com/inside-code-yt/7064d1d1553a2ee117e60217cfd1d099
    count = 0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
        if y1 == y2:
            # Point is on horizontal line, return True
            # if point[1] == y1 and min(x1, x2) <= point[0] <= max(x1, x2):
            if point[1] == y1 and (point[0] <= x1) != (point[0] < x2):
                return True

        # # Alternative way of below
        # if point[1] <= max(y1, y2):
        #     if min(y1, y2) <= point[1]:
        #         # Point is on edge
        #         if point[0] == x1:
        #             return True
        #         # Point is left of edge
        #         if point[0] < x1:
        #             count += 1

        # Point is between vertical edge
        if (point[1] <= y1) != (point[1] < y2):
            # Point is on edge
            if point[0] == x1:
                return True
            # Point is left of edge
            if point[0] < x1:
                count += 1
    return count % 2 == 1


def solve_part2(coords: list[tuple[int, int]]) -> int:
    # # Inside
    # test1 = point_in_polygon([(1, 1), (1, 3), (3, 3), (3, 1)], (1, 1))
    # test2 = point_in_polygon([(1, 1), (1, 3), (3, 3), (3, 1)], (1, 2))
    # test3 = point_in_polygon([(1, 1), (1, 3), (3, 3), (3, 1)], (3, 3))
    # test4 = point_in_polygon([(1, 1), (1, 3), (3, 3), (3, 1)], (2, 2))
    # test5 = point_in_polygon([(1, 1), (1, 3), (3, 3), (3, 1)], (2, 1))
    # # Outside
    # test6 = point_in_polygon([(1, 1), (1, 3), (3, 3), (3, 1)], (0, 2))
    # test7 = point_in_polygon([(1, 1), (1, 3), (3, 3), (3, 1)], (0, 3))
    # test8 = point_in_polygon(
    #     [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)], (7, 7)
    # )
    # exit(0)

    max_value = 0
    for i, coord1 in enumerate(coords):
        # TODO: Loop through all points again starting at i+2?
        for coord2 in coords[i + 2 :]:
            # Calc area
            area = abs((coord1[0] - coord2[0] + 1) * (coord1[1] - coord2[1] + 1))
            if area <= max_value:
                continue

            # Check if all points of rectangle are in polygon
            x_start, x_end = min(coord1[0], coord2[0]), max(coord1[0], coord2[0])
            y_start, y_end = min(coord1[1], coord2[1]), max(coord1[1], coord2[1])
            points_in_rect = [
                (x, y)
                for x in range(x_start, x_end + 1)
                for y in range(y_start, y_end + 1)
            ]
            all_points_in_rect = all(
                point_in_polygon(coords, i) for i in points_in_rect
            )
            # TODO Do I really want to break?
            if not all_points_in_rect:
                break
            # Set new value
            max_value = area
    return max_value


def solve(input_text: str) -> tuple[int, int]:
    parsed = input_text.strip().split("\n")
    coords: list[tuple[int, int]] = []
    # for line in parsed:
    #     x, y = line.split(",")
    #     coords.append((int(x), int(y)))
    # for x, y in (line.split(",") for line in parsed):
    #     coords.append((int(x), int(y)))
    coords = [(int(x), int(y)) for x, y in (line.split(",") for line in parsed)]

    return solve_part1(coords), solve_part2(coords)


def main():
    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    logger.info(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 50

    solution = solve(input_text)
    answer_part1 = solution[0]
    logger.info(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    answer_example_part2 = solution_example[1]
    logger.info(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 24

    answer_part2 = solution[1]
    logger.info(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
