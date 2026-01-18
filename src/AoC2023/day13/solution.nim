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
  proc get_mirror_index_x(grid: seq[string]): int =
    let row = grid[0]
    for x in 1 .. row.high:
      let width = min(x, row.len - x)
      let left_part = grid.mapIt(it[x - width ..< x])
      let right_part: seq[string] = grid.mapIt(it[x ..< x + width].toSeq.reversed.join)
      let is_equal = left_part == right_part
      if is_equal:
        return x
    return -1

  proc get_mirror_index_y(grid: seq[string]): int =
    for y in 1 .. grid.high:
      let height = min(y, grid.len - y)
      let upper_part = grid[y - height ..< y]
      let lower_part = grid[y ..< y + height]
      let is_equal = upper_part == lower_part.reversed
      if is_equal:
        return y
    return -1

  let lines = input_text.split("\n\n")

  for i, grid_lines in lines:
    let grid = grid_lines.split("\n")

    # Part 1
    var part1_value = -1
    let x_mirror_value = grid.get_mirror_index_x
    if x_mirror_value != -1:
      part1_value = x_mirror_value
    let y_mirror_value = grid.get_mirror_index_y
    if y_mirror_value != -1:
      part1_value = 100 * y_mirror_value
    result.part1 += part1_value

    # Part 2
    var part2_value = -1
    for y, row in grid:
      for x, value in row:
        let new_value = if value == '#': '.' else: '#'
        var new_grid = grid
        new_grid[y] = (row.toSeq[0 ..< x] & new_value & row.toSeq[x + 1 ..^ 1]).join

        let new_grid_x_mirror_value = new_grid.get_mirror_index_x
        let new_grid_y_mirror_value = new_grid.get_mirror_index_y

        # Found mirror
        if new_grid_x_mirror_value != -1 and new_grid_x_mirror_value != x_mirror_value:
          part2_value = new_grid_x_mirror_value
        if new_grid_y_mirror_value != -1 and new_grid_y_mirror_value != y_mirror_value:
          part2_value = 100 * new_grid_y_mirror_value
    if part2_value == -1:
      result.part2 += part1_value
    else:
      result.part2 += part2_value

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
  assert solution_example_part2.part2 == 400

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
