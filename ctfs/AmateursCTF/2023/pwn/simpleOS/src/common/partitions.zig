pub fn from(addr: usize) []Partition {
    return @intToPtr([*]Partition, addr)[0..4];
}

pub fn first_bootable(parts: []Partition) ?*Partition {
    for (parts) |*part| {
        if (part.is_bootable()) {
            return part;
        }
    }
    return null;
}

pub const Partition = packed struct {
    attributes: u8,
    start_chs: u24,
    type: u8,
    end_chs: u24,
    start_lba: u32,
    sectors: u32,

    const Self = @This();

    pub fn is_bootable(self: *const Self) bool {
        return self.attributes & (1 << 7) != 0;
    }
};
