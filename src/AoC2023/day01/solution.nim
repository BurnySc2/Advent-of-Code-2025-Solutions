# Run with
# nim r -d:release src/AoC2023/day01/solution.nim
import strutils
import sequtils
import math
import times

const NUMBERS =
  @["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  let lines = input_text.strip().split("\n")

  # Part 1
  if part != Part.part2:
    proc get_numbers(line: string): int =
      let index1 = line.find(Digits)
      let index2 = line.rfind(Digits)
      result = (line[index1] & line[index2]).parseInt

    result.part1 = lines.map(get_numbers).sum

  # Part 2
  if part != Part.part1:
    proc get_numbers_part2(line: string): int =
      var (index1, index2) = (int.high, 0)
      var (value1, value2) = (0, 0)
      for index, line_char in line:
        let line_short = line[index .. line.high]
        # Find index1
        if index < index1:
          if line_char in DIGITS:
            index1 = index
            value1 = line_char.ord - '0'.ord
          for number, number_str in NUMBERS:
            if line_short.startsWith(number_str):
              index1 = index
              value1 = number
              break
        # Find index2
        if line_char in DIGITS:
          index2 = index
          value2 = line_char.ord - '0'.ord
        for number, number_str in NUMBERS:
          if line_short.startsWith(number_str):
            index2 = index
            value2 = number
      result = value1 * 10 + value2

    result.part2 = lines.map(get_numbers_part2).sum

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
  assert solution_example_part1.part1 == 142

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 280

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
