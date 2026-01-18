# Run with
# nim r -d:release src/AoC2023/day13/solution.nim
import strutils
import sequtils
import math
import times
import algorithm
import tables

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

type Vec = tuple[x, y: int]

proc `+`(p1, p2: Vec): Vec =
  result = (p1.x + p2.x, p1.y + p2.y)

proc get_char(grid: seq[string], p: Vec): string =
  let height = grid.len
  let width = grid[0].len
  if not (0 <= p.x and p.x < width and 0 <= p.y and p.y < height):
    return ""
  return $grid[p.y][p.x]

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =

  let lines = input_text.split("\n\n")
  for i, grid_lines in lines:
    let grid = grid_lines.strip.split("\n")
    let row = grid[0]

    for x in 1 .. row.high:
      let width = min(x, row.len - x)
      let left_part = grid.mapIt(it[x-width..<x])
      let right_part: seq[string] = grid.mapIt(it[x..<x+width].toSeq.reversed.join)
      let is_equal = left_part == right_part
      if is_equal:
        result.part1 += x

    for y in 1 .. grid.high:
      let height = min(y, grid.len - y)
      let upper_part = grid[y - height ..< y]
      let lower_part = grid[y ..< y + height]
      let is_equal = upper_part == lower_part.reversed
      if is_equal:
        result.part1 += 100 * y

  discard

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
  assert solution_example_part1.part1 == 405

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 0

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
