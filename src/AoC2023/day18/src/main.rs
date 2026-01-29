// Run file with:
// cargo run

use std::collections::HashSet;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Instruction {
    pub direction: String,
    pub count: i32,
    pub hexadecimal: String,
}

fn get_dig_positions(
    instructions: &Vec<Instruction>,
) -> (HashSet<(i32, i32)>, HashSet<(i32, i32)>) {
    let mut position = (0, 0);
    let mut positions = HashSet::<(i32, i32)>::new();
    let mut dig_positions = HashSet::new();

    for instruction in instructions {
        match instruction.direction.as_str() {
            "R" => {
                dig_positions.insert(position);
                for _ in 0..instruction.count {
                    position.0 += 1;
                    dig_positions.insert(position);
                }
            }
            "L" => {
                dig_positions.insert(position);
                for _ in 0..instruction.count {
                    position.0 -= 1;
                    dig_positions.insert(position);
                }
            }
            "D" => {
                // Don't include top
                for _ in 0..instruction.count {
                    position.1 += 1;
                    positions.insert(position);
                }
            }
            "U" => {
                // Don't include top
                for _ in 0..instruction.count {
                    positions.insert(position);
                    position.1 -= 1;
                }
            }
            _ => println!("Ain't special"),
        }
    }
    return (positions, dig_positions);
}

fn solve(content: &str) -> (u64, u64) {
    // Parse input
    let mut instructions = Vec::new();
    for line in content.split('\n') {
        let [direction, number_str, hexadecimal] = line.split(' ').collect::<Vec<_>>()[..] else {
            todo!()
        };
        let number = number_str.parse::<i32>().unwrap();

        instructions.push(Instruction {
            direction: direction.into(),
            count: number,
            hexadecimal: hexadecimal.into(),
        });
    }

    // Part 1
    let (positions, mut dig_positions) = get_dig_positions(&instructions);
    let x_min = positions.iter().map(|v| v.0).min().unwrap();
    let x_max = positions.iter().map(|v| v.0).max().unwrap();
    let y_min = positions.iter().map(|v| v.1).min().unwrap();
    let y_max = positions.iter().map(|v| v.1).max().unwrap();

    for y in y_min..y_max + 1 {
        let mut inside = false;
        for x in x_min..x_max + 1 {
            if positions.contains(&(x, y)) {
                inside = !inside;
                dig_positions.insert((x, y));
            }
            if inside {
                dig_positions.insert((x, y));
            }
        }
    }
    let solution_part1 = dig_positions.len() as u64;

    // Part 2
    // TODO too many positions
    let part2_instructions = instructions
        .iter()
        .map(|v| {
            // Convert hex code to new instruction
            let mut hexadecimal = v.hexadecimal.clone();
            // Remove brackets (), and first char which is just #
            hexadecimal = hexadecimal[2..hexadecimal.len() - 1].into();
            // Last char is the new direction
            let new_direction = hexadecimal.pop().unwrap();
            let new_count = i32::from_str_radix(&hexadecimal, 16).unwrap();
            return Instruction {
                direction: match new_direction {
                    '0' => "R".into(),
                    '1' => "D".into(),
                    '2' => "L".into(),
                    '3' => "U".into(),
                    _ => panic!(),
                },
                count: new_count,
                hexadecimal: "".into(),
            };
        })
        .collect();

    let (positions, mut dig_positions) = get_dig_positions(&part2_instructions);
    let x_min = positions.iter().map(|v| v.0).min().unwrap();
    let x_max = positions.iter().map(|v| v.0).max().unwrap();
    let y_min = positions.iter().map(|v| v.1).min().unwrap();
    let y_max = positions.iter().map(|v| v.1).max().unwrap();

    for y in y_min..y_max + 1 {
        let mut inside = false;
        for x in x_min..x_max + 1 {
            if positions.contains(&(x, y)) {
                inside = !inside;
                dig_positions.insert((x, y));
            }
            if inside {
                dig_positions.insert((x, y));
            }
        }
    }
    let solution_part2 = dig_positions.len() as u64;

    return (solution_part1, solution_part2);
}

fn main() {
    let content_example_p1 = include_str!("example_input_p1.txt");
    let solution_example_p1 = solve(content_example_p1);
    println!("Solution example p1 is: {}", solution_example_p1.0);
    assert_eq!(solution_example_p1.0, 62);

    let content_example_p2 = include_str!("example_input_p2.txt");
    let solution_example_p2 = solve(content_example_p2);
    println!("Solution example p2 is: {}", solution_example_p2.0);
    assert_eq!(solution_example_p1.1, 952408144115);

    let content = include_str!("input.txt");
    let solution = solve(content);
    println!("Solution p1 is: {}", solution.0);
}
