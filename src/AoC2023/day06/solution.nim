# Run with
# nim r -d:release src/AoC2023/day06/solution.nim
import strutils
import sequtils
import math
import times
import re

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  let parts = input_text.split("\n")
  let times =
    parts[0].split(":")[1].strip.replace(re" +", " ").split(" ").mapIt(it.parseInt)
  let distances =
    parts[1].split(":")[1].strip.replace(re" +", " ").split(" ").mapIt(it.parseInt)

  proc calc_possibilities(time, distance: int): int =
    for hold_down in 1 .. time:
      let remaining = time - hold_down
      let my_distance = remaining * hold_down
      if distance < my_distance:
        result += 1

  # Part 1
  result.part1 = 1
  for (time, distance) in zip(times, distances):
    result.part1 *= calc_possibilities(time, distance)

  # Part 2
  let part2_time = times.mapIt($it).join.parseInt
  let part2_distance = distances.mapIt($it).join.parseInt
  result.part2 = calc_possibilities(part2_time, part2_distance)

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
  assert solution_example_part1.part1 == 288

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 71503

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
