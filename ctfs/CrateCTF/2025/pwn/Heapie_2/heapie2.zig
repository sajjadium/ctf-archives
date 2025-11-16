// $ zig version
// 0.14.1
// $ zig build-exe -fno-llvm -target x86_64-linux -OReleaseFast heapie2.zig

const std = @import("std");
const builtin = @import("builtin");

pub fn main() !void {
    const allocator = std.heap.smp_allocator;

    var buffer: [4096]u8 = undefined;
    const state = try allocator.create(State);
    defer allocator.destroy(state);
    state.* = State.init(allocator, &buffer);

    std.io.getStdOut().writer().print(
        "CPU count: {any}\n",
        .{std.Thread.getCpuCount()},
    ) catch unreachable;

    while (true) {
        const line = try state.prompt(
            \\Options:
            \\  - n: new paragraph
            \\  - g: get paragraph
            \\  - s: set paragraph
            \\  - r: remove paragraph
            \\
            \\  - e: exit
        ,
            .{},
        ) orelse break;

        const Opts = enum { n, g, s, r, e };
        const opt = std.meta.stringToEnum(Opts, line) orelse continue;
        (switch (opt) {
            .n => state.newParagraph(),
            .g => state.getParagraph(),
            .s => state.setParagraph(),
            .r => state.removeParagraph(),

            .e => break,
        }) catch |err| if (err == error.BadInput) {
            try state.stdout.print(">:(\n", .{});
        } else return err;
    }
}

const State = struct {
    paragraphs: std.StringHashMapUnmanaged([]u8),

    allocator: std.mem.Allocator,
    stdout: std.fs.File.Writer,
    stdin: std.fs.File.Reader,
    current_line: std.io.FixedBufferStream([]u8),

    const Self = @This();

    fn init(allocator: std.mem.Allocator, buffer: []u8) Self {
        return .{
            .paragraphs = .{},

            .allocator = allocator,
            .stdout = std.io.getStdOut().writer(),
            .stdin = std.io.getStdIn().reader(),
            .current_line = .{ .buffer = buffer, .pos = 0 },
        };
    }

    fn prompt(self: *Self, comptime fmt: []const u8, args: anytype) !?[]u8 {
        try self.stdout.print(fmt ++ "\n> ", args);
        self.current_line.reset();
        self.stdin.streamUntilDelimiter(self.current_line.writer(), '\n', null) catch |err| switch (err) {
            error.EndOfStream => return null,
            else => return err,
        };
        return self.current_line.getWritten();
    }

    fn newParagraph(self: *Self) !void {
        const name = try self.allocator.dupe(u8, try self.prompt("Name", .{}) orelse return error.BadInput);
        const len_string = try self.prompt("Length", .{}) orelse return error.BadInput;
        const len = std.fmt.parseInt(u11, len_string, 10) catch return error.BadInput;
        try self.paragraphs.put(self.allocator, name, try self.allocator.alloc(u8, len));
    }

    fn getParagraph(self: *Self) !void {
        const name = try self.prompt("Name", .{}) orelse return error.BadInput;
        const paragraph = self.paragraphs.get(name);
        try self.stdout.print("{?s}\n", .{paragraph});
    }

    fn setParagraph(self: *Self) !void {
        const name = try self.prompt("Name", .{}) orelse return error.BadInput;
        const contents = self.paragraphs.get(name) orelse return error.BadInput;
        const paragraph = try self.prompt("Contents", .{}) orelse return error.BadInput;
        if (contents.len != paragraph.len) return error.BadInput;
        @memcpy(contents, paragraph);
    }

    fn removeParagraph(self: *Self) !void {
        const name = try self.prompt("Name", .{}) orelse return error.BadInput;
        const paragraph = self.paragraphs.get(name) orelse return error.BadInput;
        self.allocator.free(paragraph);
    }
};
