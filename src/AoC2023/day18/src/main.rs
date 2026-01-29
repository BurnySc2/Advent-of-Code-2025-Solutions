// Run file with:
// cargo run

use std::collections::HashSet;

fn solve(content: &str) -> (i32, i32) {
    let mut position = (0, 0);
    let mut positions = HashSet::<(i32, i32)>::new();
    let mut dig_positions = HashSet::new();

    for line in content.split('\n') {
        let [directon, number_str, other] = line.split(' ').collect::<Vec<_>>()[..] else {
            todo!()
        };
        let number = number_str.parse::<i32>().unwrap();

        match directon {
            "R" => {
                dig_positions.insert(position);
                for _ in 0..number {
                    position.0 += 1;
                    dig_positions.insert(position);
                }
            }
            "L" => {
                dig_positions.insert(position);
                for _ in 0..number {
                    position.0 -= 1;
                    dig_positions.insert(position);
                }
            }
            "D" => {
                // Don't include top
                for _ in 0..number {
                    position.1 += 1;
                    positions.insert(position);
                }
            }
            "U" => {
                // Don't include top
                for _ in 0..number {
                    positions.insert(position);
                    position.1 -= 1;
                }
            }
            _ => println!("Ain't special"),
        }
    }

    let x_min = positions.iter().map(|v| v.0).min().unwrap();
    let x_max = positions.iter().map(|v| v.0).max().unwrap();
    let y_min = positions.iter().map(|v| v.1).min().unwrap();
    let y_max = positions.iter().map(|v| v.1).max().unwrap();

    // let mut positions_vec = positions
    //     .iter()
    //     .map(|v| v.clone())
    //     .collect::<Vec<_>>()
    //     .clone();
    // positions_vec.sort_by_key(|v| 1_000_000 * v.1 + v.0);
    // println!("{positions_vec:?}");

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

    return (dig_positions.len() as i32, 0);
}

fn main() {
    let content_example_p1 = include_str!("example_input_p1.txt");
    let solution_example_p1 = solve(content_example_p1);
    println!("Solution example p1 is: {}", solution_example_p1.0);
    assert_eq!(solution_example_p1.0, 62);

    let content = include_str!("input.txt");
    let solution = solve(content);
    println!("Solution p1 is: {}", solution.0);
}
