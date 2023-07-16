///! This bootsector loads the main larger bootsector from the reserved
///! sectors located after the fsinfo sectors.
///! It supports booting from FAT32
const std = @import("std");
const math = std.math;

const Partitions = @import("partitions");
const Packet = @import("packet");
const Partition = Partitions.Partition;

extern const __reserved_sectors: u16;

export fn _zig_entry(drive: u8, partition: *Partition, idx: u8) noreturn {
    print("[+] enter bootsector\r\n");

    var packet = Packet.new(.{
        .drive = drive,
        .sector_count = undefined,
        .offset = 0x7E00,
        .segment = 0,
        //// sector 0 contains bootsector
        //// sector 1 contains fat32 fsinfo
        //// sector 2 is the beginning of the extended bootsector
        //// sector 6 contains backup bootsector but we will overwrite that
        .lba = partition.start_lba + 2,
    });

    var leftover = __reserved_sectors;
    while (leftover > 0) {
        //// some BIOSes will refuse if we load more than 128 sectors at a time
        //// we accomadate for this by loading in 128 sector chunks
        const sectors = math.min(128, leftover);
        packet.sector_count = sectors;
        leftover -= sectors;

        const success = packet.load();
        if (!success) {
            fail("failed to load bootloader");
        }

        //// yay segmentation
        const overflow = @addWithOverflow(packet.offset, sectors * 512);
        packet.offset = overflow[0];
        if (overflow[1] == 1) {
            packet.segment += 1;
        }
    }

    print("[+] switching to extended bootloader\r\n");

    const extended = @intToPtr(*const fn (u8, *Partition, u8) callconv(.C) noreturn, 0x7E00);
    extended(drive, partition, idx);
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
        //// mov $imm, %ax
        //// is slightly shorter than
        //// mov $imm, %ah
        //// mov $imm, %al
        : [info] "{ax}" (0x0E00 | @as(u16, ch)),
        : "bx"
    );
}
