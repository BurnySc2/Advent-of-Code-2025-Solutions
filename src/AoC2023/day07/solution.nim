# Run with
# nim r -d:release src/AoC2023/day07/solution.nim
import strutils
import sequtils
import math
import times
import sets
import algorithm
import re

type Part = enum
  part_both = 0
  part1 = 1
  part2 = 2

type Hand = tuple[cards: string, bet: int]

var cards_part1 = @["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"].mapIt(
  it[0]
).reversed
var cards_part2 = @["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"].mapIt(
  it[0]
).reversed

proc solve(input_text: string, part: Part = Part.part_both): tuple[part1, part2: int] =
  # Part 1
  proc get_hand_value_part1(cards: string): int =
    # High card = 0
    # One pair = 1
    # Two pair = 2
    # Three of a kind = 3
    # Full house = 4
    # Four of a kind = 5
    # Five of a kind = 6
    let hash_set_len = toHashSet(cards).len
    var highest_count = 0
    for c in cards:
      let char_count = cards.countIt(it == c)
      highest_count = highest_count.max(char_count)

    # Four and five of a kind
    if 4 <= highest_count:
      return highest_count + 1
    if highest_count == 3:
      # Full house
      if hash_set_len == 2 and cards.len == 5:
        return 4
      # Three of a kind
      return 3
    # All other cases
    return cards.len - hash_set_len

  var hands: seq[Hand]
  for line in input_text.split("\n"):
    let parts = line.split
    let (cards, bet) = (parts[0], parts[1].parseInt)
    hands &= (cards, bet)

  proc cmp_hands_part1(a: Hand, b: Hand): int =
    result = cmp(a.cards.get_hand_value_part1, b.cards.get_hand_value_part1)
    if result == 0:
      for (i, j) in zip(a.cards, b.cards):
        let i_value = cards_part1.find(i)
        let j_value = cards_part1.find(j)
        if i_value != j_value:
          return cmp(i_value, j_value)

  hands.sort(cmp_hands_part1)
  for rank, hand in hands:
    result.part1 += (rank + 1) * hand.bet

  # Part 2
  proc get_hand_value_part2(cards: string): int =
    let joker_count = cards.count('J')
    if joker_count == 0:
      return get_hand_value_part1(cards)

    let cards_without_joker = cards.replace(re"J", "")
    let hash_set_len = toHashSet(cards_without_joker).len
    var highest_count = 0
    for c in cards_without_joker:
      let char_count = cards_without_joker.countIt(it == c)
      highest_count = highest_count.max(char_count)

    # Four and five of a kind
    if 4 <= highest_count + joker_count:
      return highest_count + joker_count + 1
    # Full house
    if hash_set_len == 2:
      return 4
    # Three of a kind
    if highest_count + joker_count == 3:
      return 3
    # All other cases
    return cards.len - hash_set_len

  assert get_hand_value_part2("12345") == 0
  assert get_hand_value_part2("1234J") == 1
  assert get_hand_value_part2("1233J") == 3
  assert get_hand_value_part2("123JJ") == 3
  assert get_hand_value_part2("1122J") == 4
  assert get_hand_value_part2("1222J") == 5
  assert get_hand_value_part2("122JJ") == 5
  assert get_hand_value_part2("12JJJ") == 5
  assert get_hand_value_part2("1JJJJ") == 6

  proc cmp_hands_part2(a: Hand, b: Hand): int =
    result = cmp(a.cards.get_hand_value_part2, b.cards.get_hand_value_part2)
    if result == 0:
      for (i, j) in zip(a.cards, b.cards):
        let i_value = cards_part2.find(i)
        let j_value = cards_part2.find(j)
        if i_value != j_value:
          return cmp(i_value, j_value)

  hands.sort(cmp_hands_part2)
  for rank, hand in hands:
    result.part2 += (rank + 1) * hand.bet

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
  assert solution_example_part1.part1 == 6440

  let solution_example_part2 = solve(input_example_part2_text, Part.part2)
  echo fmt"The solution for the example for part2 is: {solution_example_part2.part2}"
  assert solution_example_part2.part2 == 5905

  let t0 = epoch_time()
  let solution = solve(input_text)
  let t1 = epoch_time()
  echo fmt"The solution for part1 is: {solution.part1}"
  echo fmt"The solution for part2 is: {solution.part2}"
  echo fmt"Time taken: {format_float(t1 - t0, ffDecimal, precision = 6)} seconds"
