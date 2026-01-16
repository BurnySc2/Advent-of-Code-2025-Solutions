# Run with (because of 140x140 recursion grid)
# nim r -d:release -d:nimCallDepthLimit=20000 src/AoC2023/day10/solution.nim
import strutils
import sequtils
import math
import times
import tables
import sets

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

  let allowed_movement: Table[string, seq[Vec]] = {
    # Only movement moving out of this character are noted
    "S": @[(1, 0), (-1, 0), (0, 1), (0, -1)],
    "|": @[(0, 1), (0, -1)],
    "-": @[(1, 0), (-1, 0)],
    "F": @[(1, 0), (0, 1)],
    "L": @[(1, 0), (0, -1)],
    "J": @[(-1, 0), (0, -1)],
    "7": @[(-1, 0), (0, 1)],
  }.toTable

  proc is_valid(current_char, char_at_new_pos: string, dx, dy: int): bool =
    if (dx, dy) in allowed_movement[current_char] and
        (-dx, -dy) in allowed_movement[char_at_new_pos]:
      result = true

  while 0 < queue.len:
    let (pos, dist) = queue[0]
    queue.delete(0)

    let current_char = grid.get_char(pos)
    for (dx, dy) in neighbors:
      let new_pos = pos + (dx, dy)
      let char_at_new_pos = grid.get_char(new_pos)

      # Position already visited, no need to test again
      if new_pos in positions:
        continue

      if char_at_new_pos == "" or char_at_new_pos == ".":
        continue

      if not is_valid(current_char, char_at_new_pos, dx, dy):
        continue

      positions[new_pos] = dist + 1
      queue &= (new_pos, dist + 1)

  for (key, value) in positions.pairs:
    result.part1 = result.part1.max(value)

  # Part 2
  proc get_sides(
      pos: Vec, dx, dy: int, char_at_new_pos: string
  ): tuple[left, right: seq[Vec]] =
    let new_pos = pos + (dx, dy)
    if char_at_new_pos == "|":
      result.left &= new_pos + (dy, 0)
      result.right &= new_pos + (-dy, 0)

    if char_at_new_pos == "-":
      result.left &= new_pos + (0, -dx)
      result.right &= new_pos + (0, dx)

    if char_at_new_pos == "J" and dx == 1:
      result.left &= pos + (0, -1)
      result.right &= new_pos + (1, 0)
      result.right &= new_pos + (0, 1)
    if char_at_new_pos == "J" and dy == 1:
      result.right &= pos + (-1, 0)
      result.left &= new_pos + (1, 0)
      result.left &= new_pos + (0, 1)

    if char_at_new_pos == "L" and dx == -1:
      result.right &= pos + (0, -1)
      result.left &= new_pos + (-1, 0)
      result.left &= new_pos + (0, 1)
    if char_at_new_pos == "L" and dy == 1:
      result.left &= pos + (1, 0)
      result.right &= new_pos + (-1, 0)
      result.right &= new_pos + (0, 1)

    if char_at_new_pos == "F" and dx == -1:
      result.left &= pos + (0, 1)
      result.right &= new_pos + (-1, 0)
      result.right &= new_pos + (0, -1)
    if char_at_new_pos == "F" and dy == -1:
      result.right &= pos + (1, 0)
      result.left &= new_pos + (-1, 0)
      result.left &= new_pos + (0, -1)

    if char_at_new_pos == "7" and dx == 1:
      result.right &= pos + (0, 1)
      result.left &= new_pos + (0, -1)
      result.left &= new_pos + (1, 0)
    if char_at_new_pos == "7" and dy == -1:
      result.left &= pos + (-1, 0)
      result.right &= new_pos + (0, -1)
      result.right &= new_pos + (1, 0)

  var positions_part2: Table[Vec, int]
  var left_side: Table[Vec, int]
  var right_side: Table[Vec, int]
  var old_pos: Vec = (-1, -1)
  var pos = start
  # Loop through each character
  while pos != old_pos:
    old_pos = pos
    positions_part2[pos] = 0
    let current_char = grid.get_char(pos)
    for (dx, dy) in neighbors:
      let new_pos = pos + (dx, dy)
      if new_pos in positions_part2:
        continue
      let char_at_new_pos = grid.get_char(new_pos)
      if char_at_new_pos == "" or char_at_new_pos == ".":
        continue

      if is_valid(current_char, char_at_new_pos, dx, dy):
        let sides = get_sides(pos, dx, dy, char_at_new_pos)
        for pos in sides.left:
          left_side[pos] = 0
        for pos in sides.right:
          right_side[pos] = 0

        pos = new_pos
        break

  var already_seen: HashSet[Vec]
  var regions_left_side: seq[HashSet[Vec]]
  var regions_right_side: seq[HashSet[Vec]]
  var current_set: HashSet[Vec]

  proc flood_fill(pos: Vec) =
    current_set.incl(pos)
    already_seen.incl(pos)
    for n in neighbors:
      let new_pos = pos + n
      # Already visited by flood fill
      if new_pos in already_seen:
        continue
      # Must not be part of the loop
      if new_pos in positions_part2:
        continue
      let new_pos_char = grid.get_char(new_pos)
      if new_pos_char == "":
        continue
      flood_fill(new_pos)

  # Once a side touches edge: it is no longer the correct answer side
  var left_side_is_answer, right_side_is_answer = true

  for y, row in grid:
    for x, value in row:
      # Already visited by flood fill
      if (x, y) in already_seen:
        continue
      # Must not be part of the loop
      if (x, y) in positions_part2:
        continue
      current_set.clear
      flood_fill((x, y))
      var touches_edge = false
      var touches_left_side = false
      var touches_right_side = false
      for pos in current_set:
        if pos in left_side:
          touches_left_side = true
        if pos in right_side:
          touches_right_side = true
        for n in neighbors:
          let new_pos = pos + n
          let new_pos_char = grid.get_char(new_pos)
          if new_pos_char == "":
            touches_edge = true

      if not touches_edge and touches_left_side:
        regions_left_side &= current_set
      if not touches_edge and touches_right_side:
        regions_right_side &= current_set
      # Disqualify a side
      if touches_edge and touches_left_side:
        left_side_is_answer = false
      if touches_edge and touches_right_side:
        right_side_is_answer = false

  var left = 0
  for region in regions_left_side:
    left += region.len
  var right = 0
  for region in regions_right_side:
    right += region.len

  if left_side_is_answer:
    result.part2 = left
  else:
    result.part2 = right

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
  assert solution_example_part2.part2 == 10

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
