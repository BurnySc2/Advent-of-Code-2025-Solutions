# Run with
# nim r -d:release src/AoC2023/day05/solution.nim
import strutils
import sequtils
import math
import times

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

type MapData = tuple[destination_start: int, source_start: int, length: int]

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  let sections = input_text.split("\n\n")

  var seeds: seq[int]
  var seed_to_soil: seq[MapData]
  var soil_to_fert: seq[MapData]
  var fert_to_water: seq[MapData]
  var water_to_light: seq[MapData]
  var light_to_temp: seq[MapData]
  var temp_to_hum: seq[MapData]
  var hum_to_loc: seq[MapData]

  proc parse_map_data(data: string): MapData =
    let parts = data.split(" ").mapIt(it.parseInt)
    result = (parts[0], parts[1], parts[2])

  seeds = sections[0].split(":")[1].strip.split(" ").mapIt(it.parseInt)
  seed_to_soil = sections[1].split("\n")[1 ..^ 1].mapIt(parse_map_data(it))
  soil_to_fert = sections[2].split("\n")[1 ..^ 1].mapIt(parse_map_data(it))
  fert_to_water = sections[3].split("\n")[1 ..^ 1].mapIt(parse_map_data(it))
  water_to_light = sections[4].split("\n")[1 ..^ 1].mapIt(parse_map_data(it))
  light_to_temp = sections[5].split("\n")[1 ..^ 1].mapIt(parse_map_data(it))
  temp_to_hum = sections[6].split("\n")[1 ..^ 1].mapIt(parse_map_data(it))
  hum_to_loc = sections[7].split("\n")[1 ..^ 1].mapIt(parse_map_data(it))

  proc get_locaton_for_seed(seed: int): int =
    result = seed
    for location_maps in [
      seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp,
      temp_to_hum, hum_to_loc,
    ]:
      for location_map in location_maps:
        let (s, e) =
          (location_map.source_start, location_map.source_start + location_map.length)
        if s <= result and result < e:
          result = result + location_map.destination_start - location_map.source_start
          break

  result.part1 = int.high
  result.part2 = int.high
  for i, seed in seeds:
    # Part 1
    let location = get_locaton_for_seed(seed)
    result.part1 = result.part1.min(location)
    if i mod 2 == 1:
      continue
    # Part 2
    let seed_length = seeds[i + 1]
    for seed_number in seed ..< seed + seed_length:
      let seed_location = get_locaton_for_seed(seed_number)
      result.part2 = result.part2.min(seed_location)
    echo ("done with seed", seed)

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
  assert solution_example_part1.part1 == 35

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 46

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
