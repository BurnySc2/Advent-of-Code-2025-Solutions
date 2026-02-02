// Run file with:
// cargo run
// cargo run --release
use std::time::Instant;

fn solve(content: &str) -> (i128, i128) {
    // Parse input
    let mut instructions = Vec::new();
    for line in content.split('\n') {
        instructions.push(line);
    }

    // Part 1
    let solution_part1 = 0;

    // Part 2
    let solution_part2 = 0;

    return (solution_part1, solution_part2);
}

fn main() {
    let content_example_p1 = include_str!("example_input_p1.txt");
    let solution_example_p1 = solve(content_example_p1);
    println!("Solution example p1 is: {}", solution_example_p1.0);
    assert_eq!(solution_example_p1.0, 0);

    let content_example_p2 = include_str!("example_input_p2.txt");
    let solution_example_p2 = solve(content_example_p2);
    println!("Solution example p2 is: {}", solution_example_p2.1);
    assert_eq!(solution_example_p2.1, 0);

    let content = include_str!("input.txt");

    let t0 = Instant::now();
    let solution = solve(content);
    let t1 = Instant::now();
    println!("Solution p1 is: {}", solution.0);
    println!("Solution p2 is: {}", solution.1);
    println!("Time taken: {:.6} seconds", (t1 - t0).as_secs_f64());
}
