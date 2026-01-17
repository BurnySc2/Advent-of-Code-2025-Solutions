# Run with
# nim r -d:release src/AoC2023/day11/solution.nim
import strutils
import math
import times

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

type Vec = tuple[x, y: int]

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  let grid = input_text.split("\n")
  var galaxy_positions: seq[Vec]
  for y, row in grid:
    for x, value in row:
      if value == '#':
        galaxy_positions &= (x, y)
  # Copy for part 2
  var galaxy_positions_part2 = galaxy_positions

  # Expand y
  var y = grid.high
  while 0 <= y:
    var has_galaxy = false
    # Check if galaxy exists in y position
    for pos in galaxy_positions:
      if y == pos.y:
        has_galaxy = true
        break
    # Move galaxy one further down
    if not has_galaxy:
      for pos in galaxy_positions.mitems:
        if y < pos.y:
          pos.y += 1
      for pos in galaxy_positions_part2.mitems:
        if y < pos.y:
          pos.y += 1_000_000 - 1
    y -= 1

  # Expand x
  var x = grid[0].high
  while 0 <= x:
    var has_galaxy = false
    # Check if galaxy exists in y position
    for pos in galaxy_positions:
      if x == pos.x:
        has_galaxy = true
        break
    # Move galaxy one further right
    if not has_galaxy:
      for pos in galaxy_positions.mitems:
        if x < pos.x:
          pos.x += 1
      for pos in galaxy_positions_part2.mitems:
        if x < pos.x:
          pos.x += 1_000_000 - 1
    x -= 1

  for i, g1 in galaxy_positions:
    for g2 in galaxy_positions[i + 1 ..^ 1]:
      let dist = (g2.y - g1.y).abs + (g2.x - g1.x).abs
      result.part1 += dist

  for i, g1 in galaxy_positions_part2:
    for g2 in galaxy_positions_part2[i + 1 ..^ 1]:
      let dist = (g2.y - g1.y).abs + (g2.x - g1.x).abs
      result.part2 += dist

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
  assert solution_example_part1.part1 == 374

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 82000210

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
