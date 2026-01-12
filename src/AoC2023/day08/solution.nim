# Run with
# nim r -d:release src/AoC2023/day08/solution.nim
import strutils
import sequtils
import math
import times
import tables

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

type Path = tuple[left: string, right: string]

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  let parts = input_text.split("\n\n")
  let instructions = parts[0].strip

  var paths: Table[string, Path]
  for path in parts[1].strip.split("\n"):
    let path_parts = path.split("=")
    let source = path_parts[0].strip
    let targets = path_parts[1].strip.split(",")
    let left = targets[0].strip.strip(chars = {'(', ')'})
    let right = targets[1].strip.strip(chars = {'(', ')'})
    paths[source] = (left, right)

  proc get_next_node(turn: char, current: string): string =
    if turn == 'L':
      result = paths[current].left
    if turn == 'R':
      result = paths[current].right

  # Part 1
  var current = "AAA"
  while true:
    let turn = instructions[result.part1 mod instructions.len]
    current = get_next_node(turn, current)
    result.part1 += 1
    if current == "ZZZ":
      break

  # Part 2
  proc is_done(nodes: seq[string]): bool =
    result = nodes.len == nodes.filterIt(it[^1] == 'Z').len

  var nodes = paths.keys.toSeq.filterIt(it[^1] == 'A')
  while not is_done(nodes):
    let turn = instructions[result.part2 mod instructions.len]
    nodes = nodes.mapIt(get_next_node(turn, it))
    result.part2 += 1

when is_main_module:
  import os
  import strformat

  let input_example_part1_path =
    current_source_path.parent_dir() / "example_input_p1.txt"
  let input_example_part1_text = read_file(input_example_part1_path)

  let input_example_part2_path =
    current_source_path.parent_dir() / "example_input_p2.txt"
  let input_example_part2_text = read_file(input_example_part2_path)

  let input_path = current_source_path.parent_dir() / "input.txt"
  let input_text = read_file(input_path)

  let solution_example_part1 = solve(input_example_part1_text, Part.part1)
  echo fmt"The solution for the example for part1 is: {solution_example_part1.part1}"
  assert solution_example_part1.part1 == 6

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 6

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
