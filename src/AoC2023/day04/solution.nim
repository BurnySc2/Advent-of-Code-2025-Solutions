# Run with
# nim r -d:release src/AoC2023/day04/solution.nim
import strutils
import sequtils
import math
import times

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  let rows = input_text.split("\n")
  var part2_copies: seq[int]
  for _ in 0..rows.len:
    part2_copies &= 1
  part2_copies[0] = 0

  for row_index, row in rows:
    let index = row.find(":")
    let parts = row[index + 1 .. row.high].split("|")
    let (left, right) = (parts[0], parts[1])
    let winning_numbers = left.strip.replace("  ", " ").split.mapIt(it.parseInt)
    let my_numbers = right.strip.replace("  ", " ").split.mapIt(it.parseInt).filter(
        proc(i: int): bool =
          i in winning_numbers
      )
    result.part1 += (
      if my_numbers.len <= 2:
        my_numbers.len
      else:
        2 ^ (my_numbers.len - 1)
    )
    # Part 2
    let current_card_number = row_index + 1
    for count in 1 .. my_numbers.len:
      let card_number = current_card_number + count
      if card_number <= part2_copies.high:
        part2_copies[card_number] += part2_copies[current_card_number]

  result.part2 = part2_copies.sum

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
  assert solution_example_part1.part1 == 13

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 30

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
