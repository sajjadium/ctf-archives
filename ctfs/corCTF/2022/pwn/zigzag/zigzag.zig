// zig build-exe main.zig -O ReleaseSmall
// built with zig version: 0.10.0-dev.2959+6f55b294f

const std = @import("std");
const fmt = std.fmt;

const stdout = std.io.getStdOut().writer();
const stdin = std.io.getStdIn();

const MAX_SIZE: usize = 0x500;
const ERR: usize = 0xbaad0000;
const NULL: usize = 0xdead0000;

var chunklist: [20][]u8 = undefined;

var gpa = std.heap.GeneralPurposeAllocator(.{}){};
const allocator = gpa.allocator();

pub fn menu() !void {
    try stdout.print("[1] Add\n", .{});
    try stdout.print("[2] Delete\n", .{});
    try stdout.print("[3] Show\n", .{});
    try stdout.print("[4] Edit\n", .{});
    try stdout.print("[5] Exit\n", .{});
    try stdout.print("> ", .{});
}

pub fn readNum() !usize {
    var buf: [64]u8 = undefined;
    var stripped: []const u8 = undefined;
    var amnt: usize = undefined;
    var num: usize = undefined;

    amnt = try stdin.read(&buf);
    stripped = std.mem.trimRight(u8, buf[0..amnt], "\n");

    num = fmt.parseUnsigned(usize, stripped, 10) catch {
        return ERR;
    };

    return num;
}

pub fn add() !void {
    var idx: usize = undefined;
    var size: usize = undefined;

    try stdout.print("Index: ", .{});
    idx = try readNum();

    if (idx == ERR or idx >= chunklist.len or @ptrToInt(chunklist[idx].ptr) != NULL) {
        try stdout.print("Invalid index!\n", .{});
        return;
    }

    try stdout.print("Size: ", .{});
    size = try readNum();

    if (size == ERR or size >= MAX_SIZE) {
        try stdout.print("Invalid size!\n", .{});
        return;
    }

    chunklist[idx] = try allocator.alloc(u8, size);

    try stdout.print("Data: ", .{});
    _ = try stdin.read(chunklist[idx]);
}

pub fn delete() !void {
    var idx: usize = undefined;

    try stdout.print("Index: ", .{});
    idx = try readNum();

    if (idx == ERR or idx >= chunklist.len or @ptrToInt(chunklist[idx].ptr) == NULL) {
        try stdout.print("Invalid index!\n", .{});
        return;
    }

    _ = allocator.free(chunklist[idx]);

    chunklist[idx].ptr = @intToPtr([*]u8, NULL);
    chunklist[idx].len = 0;
}

pub fn show() !void {
    var idx: usize = undefined;

    try stdout.print("Index: ", .{});
    idx = try readNum();

    if (idx == ERR or idx >= chunklist.len or @ptrToInt(chunklist[idx].ptr) == NULL) {
        try stdout.print("Invalid index!\n", .{});
        return;
    }

    try stdout.print("{s}\n", .{chunklist[idx]});
}

pub fn edit() !void {
    var idx: usize = undefined;
    var size: usize = undefined;

    try stdout.print("Index: ", .{});
    idx = try readNum();

    if (idx == ERR or idx >= chunklist.len or @ptrToInt(chunklist[idx].ptr) == NULL) {
        try stdout.print("Invalid index!\n", .{});
        return;
    }

    try stdout.print("Size: ", .{});
    size = try readNum();

    if (size > chunklist[idx].len and size == ERR) {
        try stdout.print("Invalid size!\n", .{});
        return;
    }

    chunklist[idx].len = size;

    try stdout.print("Data: ", .{});
    _ = try stdin.read(chunklist[idx]);
}

pub fn main() !void {
    var choice: usize = undefined;

    for (chunklist) |_, i| {
        chunklist[i].ptr = @intToPtr([*]u8, NULL);
        chunklist[i].len = 0;
    }

    while (true) {
        try menu();

        choice = try readNum();
        if (choice == ERR) continue;

        if (choice == 1) try add();
        if (choice == 2) try delete();
        if (choice == 3) try show();
        if (choice == 4) try edit();
        if (choice == 5) break;
    }
}
