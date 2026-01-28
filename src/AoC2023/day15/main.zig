// Run with
// zig run src/AoC2023/day15/main.zig
const std = @import("std");

pub fn solve(input_text: []const u8) struct { i32, i32 } {
    var lines = std.mem.splitScalar(u8, input_text, '\n');

    var part1_solution: i32 = 0;
    var part2_solution: i32 = 0;
    part2_solution += 1;

    while (lines.next()) |line| {
        var values = std.mem.splitScalar(u8, line, ',');
        while (values.next()) |value| {
            var current_value: i32 = 0;
            for (value) |char| {
                current_value = @mod((current_value + char) * 17, 256);
            }
            part1_solution += current_value;
        }
    }
    return .{ part1_solution, part2_solution };
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    const current_dir = std.fs.cwd();

    // Example p1
    const input_example_part1_path = "example_input_p1.txt";
    const input_text_part1_text = try current_dir.readFileAlloc(allocator, input_example_part1_path, std.math.maxInt(usize));
    defer allocator.free(input_text_part1_text);
    const result_example_p1 = solve(input_text_part1_text);
    std.debug.print("The solution for example part1 is: {d}\n", .{result_example_p1[0]});

    // Example p2
    const input_example_part2_path = "example_input_p2.txt";
    const input_text_part2_text = try current_dir.readFileAlloc(allocator, input_example_part2_path, std.math.maxInt(usize));
    defer allocator.free(input_text_part2_text);
    const result_example_p2 = solve(input_text_part2_text);
    std.debug.print("The solution for example part1 is: {d}\n", .{result_example_p2[1]});

    // Run solution
    const input_path = "input.txt";
    const input_text = try current_dir.readFileAlloc(allocator, input_path, std.math.maxInt(usize));
    defer allocator.free(input_text);

    var timer = try std.time.Timer.start();
    const result = solve(input_text);
    const elapsed_ns = timer.read();
    const elapsed_ms = @as(f64, @floatFromInt(elapsed_ns)) / 1_000_000.0;

    std.debug.print("The solution for part1 is: {d}\n", .{result[0]});
    std.debug.print("The solution for part2 is: {d}\n", .{result[1]});
    std.debug.print("Time taken: {d:.3} ms ({d} ns)\n", .{ elapsed_ms, elapsed_ns });
}
