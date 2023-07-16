const std = @import("std");
const mem = std.mem;
const elf = std.elf;
const builtin = std.builtin;
const term = @import("term.zig");
const arch = @import("arch.zig");
const serial = @import("serial.zig");
const idt = @import("idt.zig");
const pic = @import("pic.zig");
const shell = @import("shell.zig");
const paging = @import("paging.zig");
const pio = @import("pio.zig");
const disk = @import("disk.zig");
const fs = @import("fs.zig");

export fn _start(stack_bottom: usize, stack_top: usize) callconv(.C) noreturn {
    _ = paging.identity_map;

    pic.init();
    idt.init();
    serial.init();
    disk.init();

    asm volatile ("sti");

    term.printf("stack bottom: {X:0>16}\r\n", .{stack_bottom});
    term.printf("stack top: {X:0>16}\r\n", .{stack_top});

    var heap = [_]u8{0} ** (0x100000 * 2);
    var manager = std.heap.FixedBufferAllocator.init(&heap);
    var allocator = manager.allocator();
    fs.init(allocator);

    shell.start(allocator);

    @panic("finished");
}

pub fn panic(message: []const u8, stack_trace: ?*builtin.StackTrace, ret_addr: ?usize) noreturn {
    _ = stack_trace;
    _ = ret_addr;

    term.printf("\r\n!KERNEL PANIC!: {s}\r\n", .{message});

    arch.hang();
}
