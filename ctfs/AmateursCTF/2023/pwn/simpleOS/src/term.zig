const std = @import("std");
const mem = std.mem;
const fmt = std.fmt;
const serial = @import("serial.zig");
const Writer = std.io.Writer;
const Allocator = mem.Allocator;

pub const writer = Writer(void, error{}, writeFn){ .context = {} };

fn writeFn(_: void, string: []const u8) error{}!usize {
    serial.send(string);
    return string.len;
}

pub fn printf(comptime format: []const u8, args: anytype) void {
    writer.print(format, args) catch unreachable;
}

var recent: ?u8 = null;
var do_echo = true;

pub fn init() void {}

pub fn flush() void {
    recent = null;
}

pub fn echo(state: bool) void {
    do_echo = state;
}

pub fn getchar() u8 {
    if (recent) |ch| {
        defer recent = null;
        return ch;
    }
    var ch = serial.getchar();
    if (do_echo) {
        switch (ch) {
            '\n', '\r' => {
                serial.send("\r\n");
            },
            else => serial.putchar(ch),
        }
    }
    return ch;
}

pub fn putback(ch: u8) void {
    recent = ch;
}

pub fn peek() u8 {
    if (recent) |ch| {
        return ch;
    }
    recent = serial.getchar();
    return recent.?;
}
