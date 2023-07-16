const std = @import("std");
const Fs = @import("fs.zig");
const term = @import("term.zig");
const Disk = @import("disk.zig");

const RawPartition = @import("partitions").Partition;
const Partition = @import("partition.zig");

extern const __partition_offset: usize;

export fn _extended_entry(drive: u8, raw_partition: *RawPartition, idx: u8) linksection(".entry") callconv(.C) noreturn {
    main(drive, raw_partition, idx) catch |err| @panic(@errorName(err));

    @panic("failed to load next stages");
}

fn main(drive: u8, raw_partition: *RawPartition, idx: u8) !void {
    enable_a20();
    enable_unreal_mode();

    term.print("[+] enter extended bootloader\r\n", .{});
    term.print("[+] boot args:\r\n- drive: 0x{X:0>2}\r\n- partition: {any}\r\n- index: {}\r\n", .{ drive, raw_partition, idx });

    __partition_offset = @ptrToInt(raw_partition);

    var disk = Disk.new(drive);
    var partition = Partition.from(&disk, raw_partition);
    var fs = Fs.from(&partition, 0x7C00);

    var boot = try fs.root().open("APP.BIN");
    try boot.read(@intToPtr([*]u8, 0x100000)[0..boot.size]);

    term.print("[+] switching to bootstrap\r\n", .{});

    asm volatile ("jmp _code_16");

    @panic("failed extended bootloader\r\n");
}

pub fn panic(static: []const u8, _: ?*std.builtin.StackTrace, _: ?usize) noreturn {
    term.fail("[-] PANIC: {s}", .{static});
}

//// pillaged from https://wiki.osdev.org/A20_Line
fn enable_a20() void {
    asm volatile (
        \\.intel_syntax noprefix
        \\in al, 0x92
        \\test al, 2
        \\jnz after
        \\or al, 2
        \\and al, 0xFE
        \\out 0x92, al
        \\after:
        \\.att_syntax prefix
        ::: "al");
}

const Segment = packed struct {
    limit_lo: u16 = 0,
    base_lo: u24 = 0,
    accessed: bool = false,
    readwrite: bool = false,
    grows_down: bool = false,
    executable: bool = false,
    normal: bool = false,
    ring: u2 = 0,
    present: bool = false,
    limit_hi: u4 = 0,
    reserved: bool = false,
    long_mode: bool = false,
    protected_mode: bool = false,
    large: bool = false,
    base_hi: u8 = 0,
};

const Descriptor = extern struct {
    size: u16 align(1),
    gdt: u64 align(1),
};

const gdt = [3]Segment{
    .{},
    .{ .limit_lo = 0xFFFF, .limit_hi = 0, .base_lo = 0, .base_hi = 0, .readwrite = true, .grows_down = false, .executable = true, .normal = true, .ring = 0, .present = true, .large = false },
    .{ .limit_lo = 0xFFFF, .limit_hi = 0xF, .base_lo = 0, .base_hi = 0, .readwrite = true, .grows_down = false, .executable = false, .normal = true, .ring = 0, .present = true, .large = true },
};
export var descriptor = Descriptor{
    .size = @sizeOf(@TypeOf(gdt)),
    .gdt = undefined,
};

fn enable_unreal_mode() void {
    descriptor.gdt = @ptrToInt(&gdt);
    asm volatile (
        \\.intel_syntax noprefix
        \\push ds
        \\lgdt [esi]
        \\mov eax, cr0
        \\or al, 1
        \\mov cr0, eax
        \\.att_syntax prefix
        \\jmp $0x08, $pmode
        \\.intel_syntax noprefix
        \\pmode:
        \\mov bx, 0x10
        \\mov ds, bx
        \\and al, ~1
        \\mov cr0, eax
        \\.att_syntax prefix
        \\jmp $0x00, $unreal
        \\.intel_syntax noprefix
        \\unreal:
        \\pop ds
        \\.att_syntax prefix
        :
        : [desc] "{esi}" (&descriptor),
        : "eax", "bx"
    );
}
