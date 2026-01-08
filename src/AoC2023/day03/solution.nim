# Run with
# nim r -d:release src/AoC2023/day03/solution.nim
import strutils
import sequtils
import math
import times

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

proc get_char(grid: seq[seq[string]], p: tuple[x, y: int]): string =
  let height = grid.len
  let width = grid[0].len
  if not (0 <= p.x and p.x < width and 0 <= p.y and p.y < height):
    return ""
  return grid[p.y][p.x]

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  let grid = input_text.split("\n").mapIt(it.toSeq.mapIt($it))

  # Part 1 
  proc char_is_symbol(my_char: string): bool =
    return my_char != "" and my_char != "." and my_char[0] notin Digits

  for y, row in grid:
    var current_number = ""
    var has_symbol_neighbor = false
    for x, value in row:
      if value[0] in DIGITS:
        current_number &= value
      else:
        continue

      for dx in -1 .. 1:
        for dy in -1 .. 1:
          if char_is_symbol(get_char(grid, (x + dx, y + dy))):
            has_symbol_neighbor = true

      let right_char = get_char(grid, (x + 1, y))
      if right_char == "" or right_char[0] notin Digits:
        # echo (current_number, has_symbol_neighbor)
        if has_symbol_neighbor:
          result.part1 += current_number.parseInt
        current_number = ""
        has_symbol_neighbor = false

  # Part 2
  for y, row in grid:
    for x, value in row:
      if value != "*":
        continue

      proc get_number(x, y: int): tuple[start_x, end_x, y: int] =
        var start_x = x
        var end_x = x
        # Go left till no number hit
        for dx in 1 .. grid[0].len:
          let char = get_char(grid, (x - dx, y))
          if char == "" or char[0] notin Digits:
            break
          start_x = x - dx
        # Go right till no number hit
        for dx in 1 .. grid[0].len:
          let char = get_char(grid, (x + dx, y))
          if char == "" or char[0] notin Digits:
            break
          end_x = x + dx
        return (start_x, end_x, y)
        # return grid[y][start_x..end_x].join.parseInt

      var numbers: seq[tuple[start_x, end_x, y: int]]
      for dx in -1 .. 1:
        for dy in -1 .. 1:
          let char = get_char(grid, (x + dx, y + dy))
          if char == "" or char[0] notin Digits:
            continue
          let my_tuple = get_number(x + dx, y + dy)
          if my_tuple in numbers:
            continue
          numbers &= my_tuple
      if numbers.len == 2:
        result.part2 +=
          numbers.mapIt(grid[it.y][it.start_x .. it.end_x].join.parseInt).prod

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
  assert solution_example_part1.part1 == 4361

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 467835

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
