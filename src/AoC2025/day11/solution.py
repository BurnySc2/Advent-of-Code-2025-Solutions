# Solves part 1 and part 2 in less than a second
from dataclasses import dataclass
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_part1_path = Path(__file__).parent / "example_input_part1.txt"
input_example_part1_text = input_example_part1_path.read_text()
input_example_part2_path = Path(__file__).parent / "example_input_part2.txt"
input_example_part2_text = input_example_part2_path.read_text()


@dataclass
class Vertex:
    name: str
    # Directed graph
    targets: list[str]


def parse(text: str) -> list[Vertex]:
    vertices: list[Vertex] = []
    for node_name, end_nodes_str in (
        line.split(":") for line in text.strip().splitlines()
    ):
        end_nodes = [i.strip() for i in end_nodes_str.strip().split(" ")]
        vertices.append(Vertex(node_name, end_nodes))
    return vertices


def step_part1(
    current_node: Vertex,
    vertices: dict[str, Vertex],
    target_node: str,
    count: int = 0,
) -> int:
    if current_node.name == target_node:
        return count + 1
    for target in current_node.targets:
        count += step_part1(vertices[target], vertices, target_node)
    return count


def update_nodes(
    paths_to_out: dict[str, int], nodes: dict[str, list[str]], node: str, value: int
) -> None:
    paths_to_out[node] += value
    if node not in nodes:
        return
    for loop_node in nodes[node]:
        update_nodes(paths_to_out, nodes, loop_node, value)


def step_part2(
    inverted_graph: dict[str, list[str]],
    start_node: str,
    end_node: str,
) -> int:
    # Nodes already explored
    already_visited: set[str] = set()
    paths_to_out: dict[str, int] = {start_node: 1}
    # Propagate updating values through the tree
    next_node: dict[str, list[str]] = {}
    nodes_to_explore: set[str] = {start_node}

    while 1:
        if len(nodes_to_explore) == 0:
            break

        for name in list(nodes_to_explore):
            nodes_to_explore.discard(name)
            if name in already_visited:
                continue
            already_visited.add(name)

            if name == "svr":
                continue

            for target in inverted_graph[name]:
                if name in next_node:
                    next_node[name].append(target)
                else:
                    next_node[name] = [target]

                if target in paths_to_out:
                    # Update already explored nodes
                    update_nodes(paths_to_out, next_node, target, paths_to_out[name])
                else:
                    paths_to_out[target] = paths_to_out[name]
                    nodes_to_explore.add(target)
    return paths_to_out.get(end_node, 0)


def solve(input_text: str) -> tuple[int, int]:
    parsed = parse(input_text)
    vertices = {i.name: i for i in parsed}
    for v in parsed:
        for t in v.targets:
            if t not in vertices:
                vertices[t] = Vertex(t, [])

    # Remove unused nodes
    nodes_leading_to_target_out: set[str] = {"out"}
    for _ in range(1000):
        for v in parsed:
            for t in v.targets:
                if t in nodes_leading_to_target_out:
                    nodes_leading_to_target_out.add(v.name)
                    break
    unused_nodes: set[str] = set(vertices) - nodes_leading_to_target_out
    assert len(unused_nodes) == 0

    solution_part1 = 0
    if "you" in vertices:
        start_node = vertices["you"]
        solution_part1 = step_part1(start_node, vertices, "out")

    solution_part2 = 0
    if "svr" in vertices:
        inverted_graph: dict[str, list[str]] = {}
        for v in vertices.values():
            for t in v.targets:
                if t in inverted_graph:
                    inverted_graph[t].append(v.name)
                else:
                    inverted_graph[t] = [v.name]
        count_end_to_mid_node1 = step_part2(inverted_graph, "out", "dac")
        count_end_to_mid_node2 = step_part2(inverted_graph, "out", "fft")
        count_mid_node1_to_mid_node2 = step_part2(inverted_graph, "dac", "fft")
        count_mid_node2_to_mid_node1 = step_part2(inverted_graph, "fft", "dac")
        count_mid_node1_to_start = step_part2(inverted_graph, "dac", "svr")
        count_mid_node2_to_start = step_part2(inverted_graph, "fft", "svr")
        solution_part2 = (
            count_end_to_mid_node1
            * count_mid_node1_to_mid_node2
            * count_mid_node2_to_start
            + count_end_to_mid_node2
            * count_mid_node2_to_mid_node1
            * count_mid_node1_to_start
        )
    return solution_part1, solution_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_text=input_example_part1_text)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 5

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_text=input_example_part2_text)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 2

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()
