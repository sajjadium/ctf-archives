const std = @import("std");
const Writer = std.io.Writer;

const writer = Writer(void, error{}, writeFn){ .context = {} };

fn writeFn(_: void, static: []const u8) error{}!usize {
    for (static) |ch| {
        putchar(ch);
    }
    return static.len;
}

pub fn print(comptime static: []const u8, args: anytype) void {
    writer.print(static, args) catch unreachable;
}

pub fn fail(comptime static: []const u8, args: anytype) noreturn {
    print(static, args);
    while (true) {}
}

fn putchar(ch: u8) void {
    asm volatile (
        \\xor %bx,   %bx
        \\int $0x10
        :
        //// mov $imm, %ax
        //// is slightly shorter than
        //// mov $imm, %ah
        //// mov $imm, %al
        : [info] "{ax}" (0x0E00 | @as(u16, ch)),
        : "bx"
    );
}
