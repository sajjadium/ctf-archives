const std = @import("std");
const pio = @import("pio.zig");
const arch = @import("arch.zig");
const term = @import("term.zig");
const mem = std.mem;

pub const com1 = 0x3F8;

var _wait = true;
var _read: usize = 0;
var _write: usize = 0;
pub var wait: *volatile bool = &_wait;
pub var read: *volatile usize = &_read;
pub var write: *volatile usize = &_write;
pub var buffer = [_]u8{0} ** 0x10000;

pub fn init() void {
    pio.outb(com1 + 1, 0x00); // Disable all interrupts
    pio.outb(com1 + 3, 0x80); // Enable DLAB (set baud rate divisor)
    pio.outb(com1 + 0, 0x03); // Set divisor to 3 (lo byte) 38400 baud
    pio.outb(com1 + 1, 0x00); //                  (hi byte)
    pio.outb(com1 + 3, 0x03); // 8 bits, no parity, one stop bit
    pio.outb(com1 + 2, 0xC7); // Enable FIFO, clear them, with 14-byte threshold
    pio.outb(com1 + 4, 0x0B); // IRQs enabled, RTS/DSR set
    pio.outb(com1 + 4, 0x1E); // Set in loopback mode, test the serial chip
    pio.outb(com1 + 0, 0xAE); // Test serial chip (send byte 0xAE and check if serial returns same byte)

    // Check if serial is faulty (i.e: not same byte as sent)
    if (pio.inb(com1 + 0) != 0xAE) {
        @panic("faulty serial");
    }

    // If serial is not faulty set it in normal operation mode
    // (not-loopback with IRQs enabled and OUT#1 and OUT#2 bits enabled)
    pio.outb(com1 + 4, 0x0F);
    pio.outb(com1 + 3, 0x00);
    pio.outb(com1 + 1, 0x01);
}

pub fn send(msg: []const u8) void {
    for (msg) |byte| {
        putchar(byte);
    }
}

pub fn putchar(byte: u8) void {
    while (pio.inb(com1 + 5) & 0x20 == 0) {}
    pio.outb(com1 + 0, byte);
}

pub fn getchar() u8 {
    const idx = read.*;
    while (idx == write.*) {}
    defer read.* += 1;
    return buffer[idx];
}
