const Disk = @import("disk.zig");
const RawPartition = @import("partitions").Partition;

const Self = @This();

disk: *Disk = undefined,
partition: *RawPartition = undefined,

pub fn from(media: *Disk, part: *RawPartition) Self {
    return .{
        .disk = media,
        .partition = part,
    };
}

pub fn load(self: *Self, options: struct {
    sector_count: u16,
    buffer: [*]u8,
    sector: u32,
}) void {
    self.disk.load(.{
        .sector_count = options.sector_count,
        .buffer = options.buffer,
        .sector = self.partition.start_lba + options.sector,
    });
}
