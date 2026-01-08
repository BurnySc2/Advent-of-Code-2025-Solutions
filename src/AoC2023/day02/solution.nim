# Run with
# nim r -d:release src/AoC2023/day02/solution.nim
import strutils
import sequtils
import math
import times
import tables

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  let lines = input_text.strip().split("\n")

  var part1, part2 = 0
  let part1_limit = {"red": 12, "green": 13, "blue": 14}.toTable

  proc parse_game(line: string): tuple[game_number: int, possible: bool] =
    result.possible = true
    let parts = line.split(":")
    let (game_info, cube_infos) = (parts[0], parts[1])
    let game_number = game_info.split(" ")[1].parseInt
    var part2_min_count = {"red": 0, "green": 0, "blue": 0}.toTable
    for cube_info in cube_infos.strip().replace(";", ",").split(","):
      let stripped = cube_info.strip
      let count = stripped.split(" ")[0].parseInt
      let kind = stripped.split(" ")[1]
      if kind in part1_limit and part1_limit[kind] < count:
        result.possible = false
      # Part 2
      if part2_min_count[kind] < count:
        part2_min_count[kind] = count

    if result.possible:
      part1 += game_number
    part2 += part2_min_count.values.toSeq.prod
    return (game_number, true)

  discard lines.map(parse_game)

  result.part1 = part1
  result.part2 = part2

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
  assert solution_example_part2.part2 == 2286

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
