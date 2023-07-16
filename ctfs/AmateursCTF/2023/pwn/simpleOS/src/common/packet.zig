pub fn new(options: struct {
    drive: u8,
    sector_count: u16,
    offset: u16,
    segment: u16,
    lba: u48,
}) align(4) Packet {
    return .{
        .drive = options.drive,
        .size = 0x10,
        .sector_count = options.sector_count,
        .offset = options.offset,
        .segment = options.segment,
        .lba = options.lba,
    };
}

pub const Packet = packed struct {
    size: u16,
    sector_count: u16,
    offset: u16,
    segment: u16,
    lba: u64,
    drive: u8,

    const Self = @This();

    pub fn load(self: *const Self) bool {
        const packet = @ptrToInt(self);
        return asm volatile (
            \\movb  $0x42, %ah
            \\int   $0x13
            \\setnc %al
            : [success] "={al}" (-> bool),
            : [packet] "{si}" (packet),
              [drive] "{dl}" (self.drive),
            : "ah"
        );
    }
};
