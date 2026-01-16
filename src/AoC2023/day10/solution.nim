# Run with
# nim r -d:release src/AoC2023/day10/solution.nim
import strutils
import sequtils
import math
import times
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
  let grid = input_text.split("\n")

  var neighbors: seq[Vec]
  for dx in -1 .. 1:
    for dy in -1 .. 1:
      if dx != 0 and dy != 0:
        continue
      if dx == 0 and dy == 0:
        continue
      neighbors &= (dx, dy)

  # Part 1
  var start: Vec = (-1, -1)
  var queue: seq[tuple[position: Vec, distance: int]]
  var positions: Table[Vec, int]
  for y, row in grid:
    for x, value in row:
      if value == 'S':
        start = (x, y)
        queue &= (start, 0)
        positions[start] = 0

  while 0 < queue.len:
    let (pos, dist) = queue[0]
    queue.delete(0)

    let char_at_pos = grid.get_char(pos)
    for (dx, dy) in neighbors:
      let new_pos = pos + (dx, dy)
      let char_at_new_pos = grid.get_char(new_pos)

      # Position already visited, no need to test again
      if new_pos in positions:
        continue

      if char_at_new_pos == "":
        continue

      var is_valid = false

      if char_at_new_pos == "|" and dx == 0:
        is_valid = true
      if char_at_new_pos == "-" and dy == 0:
        is_valid = true

      if char_at_new_pos == "F" and dx == 0 and dy == -1:
        is_valid = true
      if char_at_new_pos == "F" and dx == -1 and dy == 0:
        is_valid = true

      if char_at_new_pos == "7" and dx == 0 and dy == -1:
        is_valid = true
      if char_at_new_pos == "7" and dx == 1 and dy == 0:
        is_valid = true

      if char_at_new_pos == "J" and dx == 0 and dy == 1:
        is_valid = true
      if char_at_new_pos == "J" and dx == 1 and dy == 0:
        is_valid = true

      if char_at_new_pos == "L" and dx == 0 and dy == 1:
        is_valid = true
      if char_at_new_pos == "L" and dx == -1 and dy == 0:
        is_valid = true

      if not is_valid:
        continue

      positions[new_pos] = dist + 1
      queue &= (new_pos, dist + 1)

  for (key, value) in positions.pairs:
    result.part1 = result.part1.max(value)

  # Part 2

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
  assert solution_example_part1.part1 == 8

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 4

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
