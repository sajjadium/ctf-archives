const term = @import("term.zig");

const Disk = @This();

drive: u8,

pub fn new(drive: u8) Disk {
    term.print("[+] init disk\r\n", .{});
    if (asm volatile (
        \\mov  $0x41, %ah
        \\mov  $0x55AA, %bx
        \\int  $0x13
        \\setc %al
        : [_] "={al}" (-> bool),
        : [_] "{dl}" (drive),
        : "ah", "bx"
    )) {
        @panic("int 13h extensions not supported");
    }

    return .{
        .drive = drive,
    };
}

pub fn load(self: *Disk, options: struct {
    sector_count: u16,
    buffer: [*]u8,
    sector: u32,
}) void {
    const addr = @ptrToInt(options.buffer);
    var packet: Packet align(4) = Packet{
        .size = 0x10,
        .sector_count = undefined,
        .offset = @truncate(u16, addr),
        .segment = @truncate(u16, addr >> 4 & 0xF000),
        .sector = options.sector,
    };

    var leftover = options.sector_count;
    while (leftover > 0) {
        const sectors = @min(64, leftover);
        packet.sector_count = sectors;
        leftover -= sectors;

        self.internal_load(&packet);
        if (packet.sector_count != sectors) {
            @panic("sector transfer failure");
        }

        const overflow = @addWithOverflow(packet.offset, sectors * 512);
        packet.offset = overflow[0];
        if (overflow[1] == 1) {
            packet.segment += 1;
        }
    }
}

fn internal_load(self: *const Disk, packet: *Packet) void {
    var success = true;
    var error_code: u8 = 0;
    asm volatile (
        \\mov   $0x42, %ah
        \\int   $0x13
        \\setnc %al
        : [success] "={al}" (success),
          [err] "={ah}" (error_code),
        : [packet] "{si}" (packet),
          [drive] "{dl}" (self.drive),
        : "ah"
    );
    check(success, error_code);
}

const DiskError = error{};

fn check(success: bool, error_code: u8) void {
    if (success) {
        return;
    }

    term.print("success: {}\r\nerror code: {X:>02}\r\n", .{ success, error_code });
    @panic("disk error");
}

const Packet = packed struct {
    size: u16,
    sector_count: u16,
    offset: u16,
    segment: u16,
    sector: u64,
};
