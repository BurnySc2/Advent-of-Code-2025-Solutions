# Run with
# nim r -d:release src/AoC2023/day12/solution.nim
import strutils
import sequtils
import math
import times

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  proc parse_line(line: string): tuple[list: string, groups: seq[int]] =
    let parts = line.split(" ")
    result.list = parts[0]
    result.groups = parts[1].split(",").mapIt(it.parseInt)

  for line in input_text.split("\n"):
    let (list, groups) = line.parse_line

    proc dfs(current_count, index_list, index_group: int): int =
      # Out of bounds
      if list.high < index_list or groups.high < index_group:
        let last_char = list[^1]
        # Ends with # or ?
        if last_char in ['#', '?'] and index_group == groups.high and
            current_count == groups[index_group]:
          return 1
        # Ends with . or ?
        if last_char in ['.', '?'] and groups.high < index_group and current_count == 0:
          return 1
        return 0

      # End reached
      let current_target = groups[index_group]
      if list.high == index_list and groups.high == index_group and
          current_count == current_target:
        return 1

      let current_character = list[index_list]

      # No choice but to increment count
      if current_character == '#':
        result += dfs(current_count + 1, index_list + 1, index_group)

      # No choice but to increment index_list and maybe index_group
      if current_character == '.':
        if current_count == 0:
          result += dfs(0, index_list + 1, index_group)
        elif current_count == current_target:
          result += dfs(0, index_list + 1, index_group + 1)
        else:
          # Early terminate
          return 0

      # Choice: use current_character as '#' or as '.'
      if current_character == '?':
        # Use as '#'
        result += dfs(current_count + 1, index_list + 1, index_group)
        # Use as '.'
        if current_count == 0:
          result += dfs(0, index_list + 1, index_group)
        elif current_count == current_target:
          result += dfs(0, index_list + 1, index_group + 1)

    let arrangements = dfs(0, 0, 0)
    result.part1 += arrangements

  discard

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
  assert solution_example_part1.part1 == 21

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 0

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
