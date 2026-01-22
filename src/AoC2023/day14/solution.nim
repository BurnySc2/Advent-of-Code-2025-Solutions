# Run with
# nim r -d:release src/AoC2023/day14/solution.nim
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
  let grid = input_text.split("\n").mapIt(it.toSeq)

  proc move_direction(grid: var seq[seq[char]], x, y, dx, dy: int) =
    if x <= 0 and dx == -1:
      return
    if y <= 0 and dy == -1:
      return
    if grid[0].high <= x and dx == 1:
      return
    if grid.high <= y and dy == 1:
      return
    if grid[y][x] == 'O' and grid[y + dy][x + dx] == '.':
      grid[y + dy][x + dx] = 'O'
      grid[y][x] = '.'
      move_direction(grid, x + dx, y + dy, dx, dy)

  proc calc_score(grid: seq[seq[char]]): int =
    for y in 0 .. grid.high:
      for x in 0 .. grid[0].high:
        if grid[y][x] == 'O':
          result += grid.high - y + 1

  # Part 1
  # Move rocks
  var grid_part1 = grid
  for y in 0 .. grid_part1.high:
    for x in 0 .. grid_part1[0].high:
      grid_part1.move_direction(x, y, 0, -1)

  result.part1 = grid_part1.calc_score

  # Part 2
  var grid_part2 = grid
  for _ in 0 ..< 10 ^ 9:
    let grid_before = grid_part2
    # Move north
    for y in 0 .. grid_part2.high:
      for x in 0 .. grid_part2[0].high:
        grid_part2.move_direction(x, y, 0, -1)
    # Move west
    for x in 0 .. grid_part2[0].high:
      for y in 0 .. grid_part2.high:
        grid_part2.move_direction(x, y, -1, 0)
    # Move south
    for y in countdown(grid_part2.high, 0):
      for x in 0 .. grid_part2[0].high:
        grid_part2.move_direction(x, y, 0, 1)
    # Move east
    for x in countdown(grid_part2[0].high, 0):
      for y in 0 .. grid_part2.high:
        grid_part2.move_direction(x, y, 1, 0)

  result.part2 = grid_part2.calc_score

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
  assert solution_example_part1.part1 == 136

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 64

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
