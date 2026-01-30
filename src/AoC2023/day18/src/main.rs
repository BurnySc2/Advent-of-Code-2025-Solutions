// Run file with:
// cargo run

use std::collections::HashSet;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Instruction {
    pub direction: String,
    pub count: i32,
    pub hexadecimal: String,
}

fn get_ranges(
    instructions: &Vec<Instruction>,
) -> (HashSet<(i32, i32, i32, i32)>, HashSet<(i32, i32, i32, i32)>) {
    let mut position = (0, 0);
    let mut hashset_top_bottom = HashSet::<(i32, i32, i32, i32)>::new();
    let mut hashset_bottom_top = HashSet::<(i32, i32, i32, i32)>::new();

    for instruction in instructions {
        match instruction.direction.as_str() {
            "R" => {
                position.0 += instruction.count;
            }
            "L" => {
                position.0 -= instruction.count;
            }
            "D" => {
                // Don't include top
                hashset_top_bottom.insert((
                    position.0,
                    position.1 + 1,
                    position.0,
                    position.1 + instruction.count,
                ));
                // Don't include bottom
                hashset_bottom_top.insert((
                    position.0,
                    position.1,
                    position.0,
                    position.1 + instruction.count - 1,
                ));
                position.1 += instruction.count;
            }
            "U" => {
                // Don't include top
                hashset_top_bottom.insert((
                    position.0,
                    position.1 - instruction.count + 1,
                    position.0,
                    position.1,
                ));
                // Don't include bottom
                hashset_bottom_top.insert((
                    position.0,
                    position.1 - instruction.count,
                    position.0,
                    position.1 - 1,
                ));
                position.1 -= instruction.count;
            }
            _ => println!("Ain't special"),
        }
    }
    return (hashset_top_bottom, hashset_bottom_top);
}

fn calculate_solution(instructions: &Vec<Instruction>) -> i128 {
    let (hashset_top_bottom, hashset_bottom_top) = get_ranges(&instructions);

    let y1_min = hashset_top_bottom.iter().map(|v| v.1).min().unwrap();
    let y1_max = hashset_top_bottom.iter().map(|v| v.3).max().unwrap();
    let mut hashset_top_bottom_sorted = hashset_top_bottom.into_iter().collect::<Vec<_>>();
    hashset_top_bottom_sorted.sort_by_key(|v| v.1 as i128 * 10i128.pow(12) + v.0 as i128);

    let y2_min = hashset_bottom_top.iter().map(|v| v.1).min().unwrap();
    let y2_max = hashset_bottom_top.iter().map(|v| v.3).max().unwrap();
    let mut hashset_bottom_top_sorted = hashset_bottom_top.into_iter().collect::<Vec<_>>();
    hashset_bottom_top_sorted.sort_by_key(|v| v.1 as i128 * 10i128.pow(12) + v.0 as i128);

    let mut solution = 0i128;
    let y_min = y1_min.min(y2_min);
    let y_max = y1_max.max(y2_max);
    // println!("y_min and y_max: {y_min} {y_max}");
    for y in y_min..y_max + 1 {
        let mut verticals_top_bottom = hashset_top_bottom_sorted
            .iter()
            .filter(|v| v.1 <= y && y <= v.3)
            .collect::<Vec<_>>();
        verticals_top_bottom.sort_by_key(|v| v.0);

        let mut verticals_bottom_top = hashset_bottom_top_sorted
            .iter()
            .filter(|v| v.1 <= y && y <= v.3)
            .collect::<Vec<_>>();
        verticals_bottom_top.sort_by_key(|v| v.0);

        let mut x_ranges = Vec::new();

        // Calculate top_bottom ranges
        for i in (0..verticals_top_bottom.len()).step_by(2) {
            x_ranges.push((verticals_top_bottom[i].0, verticals_top_bottom[i + 1].0));
        }
        // Calculate bottom_top ranges
        for i in (0..verticals_bottom_top.len()).step_by(2) {
            x_ranges.push((verticals_bottom_top[i].0, verticals_bottom_top[i + 1].0));
        }
        // Merge ranges
        x_ranges.sort_by_key(|v| v.1);
        let (mut start, mut end) = (-10i128.pow(12) + 1, -10i128.pow(12));
        for (x0, x1) in x_ranges {
            if end < x0 as i128 {
                solution += end - start + 1;
                start = x0 as i128;
                end = x1 as i128;
            } else {
                start = start.min(x0 as i128);
                end = end.max(x1 as i128);
            }
        }
        if start < end {
            solution += end - start + 1
        }
    }

    return solution as i128;
}

fn solve(content: &str) -> (i128, i128) {
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
    let solution_part1 = calculate_solution(&instructions);

    // Part 2
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

    let solution_part2 = calculate_solution(&part2_instructions);

    return (solution_part1, solution_part2);
}

fn main() {
    let content_example_p1 = include_str!("example_input_p1.txt");
    let solution_example_p1 = solve(content_example_p1);
    println!("Solution example p1 is: {}", solution_example_p1.0);
    assert_eq!(solution_example_p1.0, 62);

    let content_example_p2 = include_str!("example_input_p2.txt");
    let solution_example_p2 = solve(content_example_p2);
    println!("Solution example p2 is: {}", solution_example_p2.1);
    assert_eq!(solution_example_p2.1, 952408144115);

    let content = include_str!("input.txt");
    let solution = solve(content);
    println!("Solution p1 is: {}", solution.0);
    // TODO Why is example p2 working but not for real input
    println!("Solution p2 is: {}", solution.1);
}
