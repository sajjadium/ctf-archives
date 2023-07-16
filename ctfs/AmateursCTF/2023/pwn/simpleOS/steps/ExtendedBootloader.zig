const std = @import("std");
const ExtendedBootloader = @This();
const Build = std.Build;
const Builder = Build.Builder;
const FileSource = Build.FileSource;
const GeneratedFile = Build.GeneratedFile;
const Step = Build.Step;

const fs = std.fs;

pub const Partition = packed struct {
    attributes: u8,
    start_chs: u24,
    type: u8,
    end_chs: u24,
    start_lba: u32,
    sectors: u32,

    pub fn is_bootable(self: *const @This()) bool {
        return self.attributes & (1 << 7) != 0;
    }
};

const Options = struct {
    disk_image: FileSource,
    extended_bootloader: FileSource,
};

step: Step,
disk_image: FileSource,
extended_bootloader: FileSource,

const Self = @This();
pub const base_id: Step.Id = .custom;

pub fn create(owner: *Builder, options: Options) *Self {
    const self = owner.allocator.create(Self) catch @panic("OOM");
    const step = Step.init(.{
        .id = base_id,
        .name = "add extended bootloader",
        .owner = owner,
        .makeFn = make,
    });

    self.* = Self{
        .step = step,
        .disk_image = options.disk_image,
        .extended_bootloader = options.extended_bootloader,
    };
    return self;
}

fn make(step: *Step, progress: *std.Progress.Node) !void {
    _ = progress;

    const builder = step.owner;
    const self = @fieldParentPtr(Self, "step", step);

    const disk = try fs.openFileAbsolute(self.disk_image.getPath(builder), .{
        .mode = .read_write,
    });
    const extended = try fs.openFileAbsolute(self.extended_bootloader.getPath(builder), .{
        .mode = .read_only,
    });
    const length = try extended.getEndPos();

    if (length > (64 - 2) * 512) {
        return step.fail("extended bootloader too large", .{});
    }

    try disk.seekableStream().seekTo(446);

    for (0..4) |_| {
        const partition = try disk.reader().readStruct(Partition);
        if (partition.is_bootable()) {
            const offset = (partition.start_lba + 2) * 512;
            _ = try extended.copyRange(0, disk, offset, length);
            return;
        }
    }

    return step.fail("did not find bootable partition", .{});
}
