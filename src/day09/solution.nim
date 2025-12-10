# Run with
# nim c -r -d:release src/day09/solution.nim
import math
import strutils

type Coord = tuple[x, y: int]

proc solvePart1(coords: seq[Coord]): int =
  var maxValue = 0
  for i, coord1 in coords:
    for coord2 in coords[i + 1 .. ^1]:
      let area = abs((coord1.x - coord2.x + 1) * (coord1.y - coord2.y + 1))
      if maxValue < area:
        maxValue = area
  return maxValue

proc pointInPolygon(points: seq[Coord], point: Coord): bool =
  var count = 0
  for i in 0 ..< points.len:
    let (x1, y1) = points[i]
    let (x2, y2) = points[(i + 1) mod points.len]
    
    if y1 == y2:
      if point.y == y1 and (point.x <= x1) != (point.x < x2):
        return true
    
    if (point.y <= y1) != (point.y < y2):
      if point.x == x1:
        return true
      if point.x < x1:
        count += 1
  return count mod 2 == 1

proc solvePart2(coords: seq[Coord]): int =
  var maxValue = 0
  for i, coord1 in coords:
    if i + 2 >= coords.len:
      break
    for coord2 in coords[i + 2 .. ^1]:
      let area = abs((coord1.x - coord2.x + 1) * (coord1.y - coord2.y + 1))
      if area <= maxValue:
        continue
      
      let xStart = min(coord1.x, coord2.x)
      let xEnd = max(coord1.x, coord2.x)
      let yStart = min(coord1.y, coord2.y)
      let yEnd = max(coord1.y, coord2.y)
      
      var allPointsInRect = true
      block outer:
        for x in xStart .. xEnd:
          for y in yStart .. yEnd:
            if not pointInPolygon(coords, (x, y)):
              allPointsInRect = false
              break outer
      
      if not allPointsInRect:
        continue
      
      maxValue = area
  return maxValue

proc solve(inputText: string): tuple[part1, part2: int] =
  let parsed = inputText.strip().split('\n')
  var coords: seq[Coord] = @[]
  
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