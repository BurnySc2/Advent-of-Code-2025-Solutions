# THIS YIELDS THE WRONG SOLUTION FOR PART 2!
import math
from dataclasses import dataclass
from pathlib import Path

from loguru import logger

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()
input_example_custom_path = Path(__file__).parent / "example_input_custom.txt"
input_example_custom_text = input_example_custom_path.read_text()


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
class Rect:
    x: int
    y: int
    width: int
    height: int

    @property
    def area(self) -> int:
        return (self.width + 1) * (self.height + 1)


type Vec = tuple[int, int]


@dataclass
class Edge:
    start: Vec
    end: Vec


def rect_in_polygon(
    vertical_edges: list[Edge],
    horizontal_edges: list[Edge],
    rect: Rect,
) -> bool:
    """
    Start top left (0, 0):
    Check if point is inside the polygon
    Then move rightwards in x direction to check if we ever leave the polygon, can early return false
    Repeat for (0, y+1) until bottom left is reached
    """
    right = rect.x + rect.width
    for y in range(rect.y, rect.y + rect.height + 1):
        count_before = 0
        h_edges_before = 0
        count_inside = 0
        h_edges_inside = 0
        for edge in vertical_edges:
            if not (edge.start[1] <= y <= edge.end[1]):
                # Edge not relevant for this y-value
                continue
            if edge.start[0] <= rect.x:
                # Count how many vertical edges there are on the left of the current point
                count_before += 1
            if rect.x < edge.start[0] < right:
                # Count how many edges there are inside the polygon
                count_inside += 1

        for edge in horizontal_edges:
            if y != edge.start[1]:
                continue
            if edge.start[0] < rect.x and edge.end[0] < rect.x:
                h_edges_before += 1
            if edge.start[0] <= rect.x or edge.end[0] <= rect.x:
                h_edges_inside += 1

        if 0 < count_inside:
            return False
        if (count_before + h_edges_before) % 2 == 0:
            return False
    return True


def solve_part2(coords: list[tuple[int, int]]) -> int:
    h_edges: list[Edge] = []
    v_edges: list[Edge] = []
    for p1, p2 in zip(coords, coords[1:] + coords[:1]):
        if p1[1] == p2[1]:
            # Horizontal edge, skip
            h_edges.append(Edge(p1, p2))
            continue
        if p2[1] < p1[1]:
            # Swap so that p1.y < p2.y
            p1, p2 = p2, p1
        v_edges.append(Edge(p1, p2))
    # Sort ascending by y value of first point
    v_edges.sort(key=lambda i: i.start[1])

    if len(v_edges) < 4:
        # Asserts for example input
        assert rect_in_polygon(v_edges, h_edges, Rect(7, 1, 4, 2))
        assert rect_in_polygon(v_edges, h_edges, Rect(7, 1, 4, 2))
        assert rect_in_polygon(v_edges, h_edges, Rect(2, 3, 7, 2))
        # TODO assert not rect_in_polygon(v_edges, h_edges, Rect(2, 5, 7, 2))

    max_value = 0
    for i, coord1 in enumerate(coords):
        # TODO: Loop through all points again starting at i+2?
        for coord2 in coords[i + 2 :] + coords[: i + 2]:
            # Calc area
            rect = Rect(
                min(coord1[0], coord2[0]),
                min(coord1[1], coord2[1]),
                abs(coord1[0] - coord2[0]),
                abs(coord1[1] - coord2[1]),
            )
            area = rect.area
            if area <= max_value:
                continue

            if not rect_in_polygon(v_edges, h_edges, rect):
                continue
            # Set new value
            max_value = area
    return max_value


def solve(input_text: str) -> tuple[int, int]:
    parsed = input_text.strip().split("\n")
    coords: list[tuple[int, int]] = []
    coords = [(int(x), int(y)) for x, y in (line.split(",") for line in parsed)]

    return solve_part1(coords), solve_part2(coords)


def run_test_cases_on_custom(input_text: str):
    parsed = input_text.strip().split("\n")
    coords: list[tuple[int, int]] = []
    coords = [(int(x), int(y)) for x, y in (line.split(",") for line in parsed)]

    h_edges: list[Edge] = []
    v_edges: list[Edge] = []
    for p1, p2 in zip(coords, coords[1:] + coords[:1]):
        if p1[1] == p2[1]:
            # Horizontal edge, skip
            h_edges.append(Edge(p1, p2))
            continue
        if p2[1] < p1[1]:
            # Swap so that p1.y < p2.y
            p1, p2 = p2, p1
        v_edges.append(Edge(p1, p2))
    # Sort ascending by y value of first point
    v_edges.sort(key=lambda i: i.start[1])

    test_cases_in_polygon = [
        # Simple inside
        (6, 2, 1, 1),
        (6, 3, 1, 1),
        (6, 4, 1, 1),
        # On edge
        (7, 2, 1, 1),
        (6, 2, 2, 1),
        (1, 4, 1, 1),
        # Touching corners
        (1, 3, 1, 1),
        (1, 3, 2, 2),
        (1, 3, 3, 3),
        (5, 1, 1, 1),
        (5, 1, 2, 2),
        (5, 1, 3, 3),
        (5, 1, 4, 4),
        (4, 6, 1, 1),
        (4, 6, 2, 2),
        (6, 7, 1, 1),
    ]

    # test_cases_outside_polygon = [
    #     # TODO
    #     (2,3,4,5)
    # ]

    for t in test_cases_in_polygon:
        rect = Rect(*t)
        assert rect_in_polygon(v_edges, h_edges, rect), rect

    # TODO
    # for t in test_cases_outside_polygon:
    #     rect = Rect(*t)
    #     assert not rect_in_polygon(v_edges, h_edges, rect)

    print("Tests completed")


def main():
    # Custom grid
    run_test_cases_on_custom(input_text=input_example_custom_text)

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
