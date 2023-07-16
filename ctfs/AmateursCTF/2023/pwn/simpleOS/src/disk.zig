const pio = @import("pio.zig");
const term = @import("term.zig");

extern const __partition_offset: u16;

pub const Partition = packed struct {
    flags: u8,
    start_head: u8,
    start_sector: u6,
    start_cylinder: u10,
    id: u8,
    end_head: u8,
    end_sector: u6,
    end_cylinder: u10,
    start: u32,
    total: u32,
};

pub const Error = error{
    ReadError,
    WriteError,
    MustBeMultipleOf512,
};

pub var partition: Partition = undefined;

pub fn init() void {
    partition = @intToPtr(*Partition, @as(usize, __partition_offset)).*;
}

pub fn read(relative: usize, buffer: []align(1) u16) !void {
    if (buffer.len % 256 != 0) {
        return Error.MustBeMultipleOf512;
    }

    var sectors = buffer.len / 256;
    var current = relative;
    var raw = @ptrCast([*]align(1) u16, buffer);
    while (sectors > 0) {
        const count = @min(sectors, 256);
        try _read(current, raw, @truncate(u8, count));
        current += count;
        raw += count * 256;
        sectors -= count;
    }
}

pub fn write(relative: usize, buffer: []align(1) u16) !void {
    var adjusted = buffer.len + 255 & ~@as(usize, 255);
    var sectors = adjusted / 256;
    var current = relative;
    var raw = @ptrCast([*]align(1) u16, buffer);
    while (sectors > 0) {
        const count = @min(sectors, 256);
        try _write(current, raw, @truncate(u8, count));
        flush();
        current += count;
        raw += count * 256;
        sectors -= count;
    }
}

fn setup(absolute: usize, sectors: u8) void {
    const lo = @truncate(u8, absolute);
    const mi = @truncate(u8, absolute >> 8);
    const hi = @truncate(u8, absolute >> 16);
    const up = @truncate(u8, absolute >> 24);
    pio.outb(0x1f6, 0xe0 | up);
    pio.outb(0x1f0, 0);
    pio.outb(0x1f2, sectors);
    pio.outb(0x1f3, lo);
    pio.outb(0x1f4, mi);
    pio.outb(0x1f5, hi);
}

fn wait() u8 {
    var status: u8 = pio.in8(0x1f7);
    while (status & 0x88 != 0) {
        status = pio.in8(0x1f7);
    }
    return status;
}

fn _read(relative: usize, buffer: [*]align(1) u16, sectors: u8) !void {
    var status = wait();

    const absolute = @truncate(u28, partition.start + relative);
    setup(absolute, sectors);
    pio.outb(0x1f7, 0x20);

    for (0..4) |_| {
        status = pio.inb(0x1f7);
        if (status & 0x80 != 0) continue;
        if (status & 0x08 != 0) break;
    }

    for (0..sectors) |sector| {
        while (true) {
            status = pio.inb(0x1f7);
            if (status & 0x80 != 0) continue;
            if (status & 0x21 != 0) return Error.ReadError;
            break;
        }

        for (0..256) |i| {
            const word = pio.in16(0x1f0);
            buffer[sector * 256 + i] = word;
        }

        inline for (0..16) |_| {
            status = pio.inb(0x1f7);
        }
    }

    if (status & 0x21 != 0) {
        return Error.ReadError;
    }
}

fn _write(relative: usize, buffer: [*]align(1) u16, sectors: u8) !void {
    var status: u8 = wait();

    const absolute = @truncate(u28, partition.start + relative);
    term.printf("writing to {} sectors to logical block {}\r\n", .{ sectors, absolute });
    setup(absolute, sectors);
    pio.outb(0x1f7, 0x30);

    for (0..4) |_| {
        status = pio.inb(0x1f7);
        if (status & 0x80 != 0) continue;
        if (status & 0x08 != 0) break;
    }

    for (0..sectors) |sector| {
        while (true) {
            status = pio.inb(0x1f7);
            if (status & 0x80 != 0) continue;
            if (status & 0x21 != 0) return Error.WriteError;
            break;
        }

        for (0..256) |i| {
            pio.out16(0x1f0, buffer[sector * 256 + i]);
        }

        inline for (0..16) |_| {
            status = pio.inb(0x1f7);
        }
    }

    if (status & 0x21 != 0) {
        return Error.WriteError;
    }
}

fn flush() void {
    var status: u8 = wait();
    pio.outb(0x1f7, 0xe7);
    while (status & 0x80 != 0) {
        status = pio.inb(0x1f7);
    }
}
