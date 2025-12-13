# PART 2 TOO SLOW! Use different approach
# Run with
# nim c -r -d:release src/day11/solution.nim
import math
import strutils
import std/tables
import strformat

type 
    Vertex = object
        name: string
        targets: seq[string]

proc parse(text: string): seq[Vertex] =
  var vertices: seq[Vertex] = @[]
  for line in text.split("\n"):
    let line_split = line.split(":")
    let node_name = line_split[0]
    var end_nodes: seq[string] = @[]
    for name in line_split[1].strip().split(" "):
      end_nodes &= name
    vertices &= Vertex(name: node_name, targets: end_nodes)
  return vertices

proc step_part1(
    current_node: Vertex,
    vertices: Table[string, Vertex],
    target_node: string,
    count: var int,
) =
    if current_node.name == target_node:
      count += 1
      return
    for target in current_node.targets:
      step_part1(vertices[target], vertices, target_node, count)

proc step_part2(
    vertices: Table[string, Vertex],
): int =
  let start_node = "svr"
  let mid_node1 = "dac"
  let mid_node2 = "fft"
  let end_node = "out"

  var count_start_to_mid_node1 = 0
  var count_start_to_mid_node2 = 0
  var count_mid_node1_to_mid_node2 = 0
  var count_mid_node2_to_mid_node1 = 0
  var count_mid_node1_to_end = 0
  var count_mid_node2_to_end = 0

  echo "1"
  step_part1(vertices[start_node], vertices, mid_node1, count_start_to_mid_node1)
  echo "2"
  step_part1(vertices[start_node], vertices, mid_node2, count_start_to_mid_node2)
  echo "3"
  step_part1(vertices[mid_node1], vertices, mid_node2, count_mid_node1_to_mid_node2)
  echo "4"
  step_part1(vertices[mid_node2], vertices, mid_node1, count_mid_node2_to_mid_node1)
  echo "5"
  step_part1(vertices[mid_node1], vertices, end_node, count_mid_node1_to_end)
  echo "6"
  step_part1(vertices[mid_node2], vertices, end_node, count_mid_node2_to_end)
  echo "7"

  return count_start_to_mid_node1 * count_mid_node1_to_mid_node2 * count_mid_node2_to_end + count_start_to_mid_node2 * count_mid_node2_to_mid_node1 * count_mid_node1_to_end
  
proc solve(input_text: string): tuple[part1, part2: int] =
  let parsed = parse(input_text.strip())
  var vertices = initTable[string, Vertex]()
  for i in parsed:
    vertices[i.name] = i
  
  for v in parsed:
      for t in v.targets:
          if not (t in vertices):
              vertices[t] = Vertex(name: t, targets: @[])

  result.part1 = 0
  if "you" in vertices:
    step_part1(vertices["you"], vertices, "out", result.part1)

  result.part2 = 0
  if "svr" in vertices:
    result.part2 = step_part2(vertices)

when isMainModule: 
  import os
  import strformat

  let inputExamplePart1Path = currentSourcePath.parentDir() / "example_input_part1.txt"
  let inputExamplePart1Text = readFile(inputExamplePart1Path)

  let inputExamplePart2Path = currentSourcePath.parentDir() / "example_input_part2.txt"
  let inputExamplePart2Text = readFile(inputExamplePart2Path)

  let inputPath = currentSourcePath.parentDir() / "input.txt"
  let inputText = readFile(inputPath)

  let solutionPart1Example = solve(inputExamplePart1Text)
  echo fmt"The solution for the example for part1 is: {solutionPart1Example.part1}"
  assert solutionPart1Example.part1 == 5

  let solutionPart2Example = solve(inputExamplePart2Text)
  echo fmt"The solution for the example for part2 is: {solutionPart2Example.part2}"
  assert solutionPart2Example.part2 == 2

  let solution = solve(inputText)
  echo fmt"The solution for part2 is: {solution.part2}"

