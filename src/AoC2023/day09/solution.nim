# Run with
# nim r -d:release src/AoC2023/day09/solution.nim
import strutils
import sequtils
import math
import times
import algorithm

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  for line in input_text.split("\n"):
    var last_line = @[-1]
    let first_line = line.split(" ").mapIt(it.parseInt)
    var lines: seq[seq[int]]
    lines &= first_line
    while last_line.filterIt(it != 0).len != 0:
      last_line = @[]
      for (value, next_value) in zip(lines[^1][0 ..^ 2], lines[^1][1 ..^ 1]):
        let diff = next_value - value
        last_line &= diff
      lines &= last_line

    var part1_summand = 0
    for row in lines.reversed:
      part1_summand += row[^1]
    result.part1 += part1_summand

    var part2_summand = 0
    for row in lines.reversed:
      part2_summand = row[0] - part2_summand
    result.part2 += part2_summand

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
  assert solution_example_part1.part1 == 114

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 2

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
