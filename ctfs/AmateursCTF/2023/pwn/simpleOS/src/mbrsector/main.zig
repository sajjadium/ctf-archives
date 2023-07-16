const Partitions = @import("partitions");
const Packet = @import("packet");

extern const __partition_table: usize;

export fn _zig_entry(drive: u8) callconv(.C) noreturn {
    print("[+] entering mbrsector\r\n");

    const addr = @truncate(u16, @ptrToInt(&__partition_table));
    const parts = Partitions.from(addr);
    for (parts, 0..) |partition, idx| {
        if (!partition.is_bootable()) {
            continue;
        }

        if (Packet.new(.{
            .drive = drive,
            .sector_count = 1,
            .offset = 0x7C00,
            .segment = 0,
            .lba = partition.start_lba,
        }).load()) {
            print("[+] switching to bootsector\r\n");
            asm volatile (
                \\jmp   $0, $0x7C00
                :
                : [drive] "{dl}" (drive),
                  [part] "{si}" (addr + idx * @sizeOf(Partitions.Partition)),
                  [idx] "{cx}" (idx),
            );
        } else {
            fail("failed to load bootsector");
        }
    }

    fail("no bootable partitions");
}

fn fail(static: []const u8) noreturn {
    print(static);
    while (true) {}
}

fn print(static: []const u8) void {
    for (static) |ch| {
        putchar(ch);
    }
}

fn putchar(ch: u8) void {
    asm volatile (
        \\xor %bx,   %bx
        \\int $0x10
        :
        : [info] "{ax}" (0x0E00 | @as(u16, ch)),
        : "bx", "ax"
    );
}
