# THIS YIELDS THE WRONG SOLUTION!
# Run with
# nim r -d:release src/AoC2025/day09/solution.nim
import math
import strutils
import algorithm

type
  Vec = tuple[x, y: int]

  Rect = object
    x: int
    y: int
    width: int
    height: int

proc area(rect: Rect): int =
  return (rect.width + 1) * (rect.height + 1)

type Edge = object
  start: Vec
  finish: Vec

proc rectInPolygon(
    verticalEdges: seq[Edge], horizontalEdges: seq[Edge], rect: Rect
): bool =
  let right = rect.x + rect.width
  for y in rect.y .. rect.y + rect.height:
    var countBefore = 0
    var hEdgesBefore = 0
    var countInside = 0

    for edge in verticalEdges:
      if not (edge.start.y <= y and y <= edge.finish.y):
        # Edge not relevant for this y-value
        continue
      if edge.start.x <= rect.x:
        # Count how many vertical edges there are on the left of the current point
        countBefore += 1
      if rect.x < edge.start.x and edge.start.x < right and y < edge.start.y:
        # Count how many edges there are inside the polygon
        countInside += 1

    for edge in horizontalEdges:
      if y != edge.start.y:
        continue
      if edge.start.x < rect.x or edge.finish.x < rect.x:
        hEdgesBefore += 1

    if countInside > 0:
      return false
    if (countBefore + hEdgesBefore) mod 2 == 0 and rect.width > 0 or countBefore == 0:
      return false
  return true

proc solvePart1(coords: seq[Vec]): int =
  var maxValue = 0
  for i, coord1 in coords:
    for coord2 in coords[i + 1 .. ^1]:
      let area = abs((coord1.x - coord2.x + 1) * (coord1.y - coord2.y + 1)).int
      if maxValue < area:
        maxValue = area
  return maxValue

proc solvePart2(coords: seq[Vec]): int =
  var hEdges: seq[Edge] = @[]
  var vEdges: seq[Edge] = @[]

  for i in 0 ..< coords.len:
    var p1 = coords[i]
    var p2 = coords[(i + 1) mod coords.len]

    if p1.y == p2.y:
      # Horizontal edge, skip
      hEdges.add(Edge(start: p1, finish: p2))
      continue
    if p2.y < p1.y:
      # Swap so that p1.y < p2.y
      let temp = p1
      p1 = p2
      p2 = temp
    vEdges.add(Edge(start: p1, finish: p2))

  # Sort ascending by y value of first point
  vEdges = vEdges.sorted(
    proc(a, b: Edge): int =
      cmp(a.start.y, b.start.y)
  )

  var maxValue = 0
  for i, coord1 in coords:
    for j in 0 ..< coords.len:
      let coord2 = coords[j mod coords.len]
      # Calc area
      let rect = Rect(
        x: min(coord1.x, coord2.x),
        y: min(coord1.y, coord2.y),
        width: abs(coord1.x - coord2.x),
        height: abs(coord1.y - coord2.y),
      )
      let area = area(rect)
      if area <= maxValue:
        continue

      if not rectInPolygon(vEdges, hEdges, rect):
        continue
      # Set new value
      maxValue = area
  return maxValue

proc solve(inputText: string): tuple[part1, part2: int] =
  let parsed = inputText.strip().split('\n')
  var coords: seq[Vec] = @[]

  for line in parsed:
    let parts = line.split(',')
    if parts.len >= 2:
      coords.add((parts[0].parseInt(), parts[1].parseInt()))

  result.part1 = solvePart1(coords)
  result.part2 = solvePart2(coords)

when isMainModule:
  import os
  import strformat

  let inputPath = currentSourcePath.parentDir() / "input.txt"
  let inputText = readFile(inputPath)

  let inputExamplePath = currentSourcePath.parentDir() / "example_input.txt"
  let inputExampleText = readFile(inputExamplePath)

  let solutionExample = solve(inputExampleText)
  echo fmt"The solution for the example for part1 is: {solutionExample.part1}"
  assert solutionExample.part1 == 50

  echo fmt"The solution for the example for part2 is: {solutionExample.part2}"
  assert solutionExample.part2 == 24

  let solution = solve(inputText)
  echo fmt"The solution for part1 is: {solution.part1}"

  echo fmt"The solution for part2 is: {solution.part2}"
