const std = @import("std");
const mem = std.mem;
const pathutil = std.fs.path;
const term = @import("term.zig");
const disk = @import("disk.zig");

pub const Fs = @This();
const Partition = @import("partition.zig");

cluster_bit_used: u8,
cluster_bit_width: u8,
fat_size: u32,

first_data_sector: u32,
first_fat_sector: u32,
first_root_cluster: u32,

sectors_per_cluster: u8,
bytes_per_sector: u16,

total_sectors: u32,
data_sectors: u32,
reserved_sectors: u32,
root_dir_sectors: u32,
total_clusters: u32,

kind: Kind,
partition: *Partition,

const Kind = enum {
    fat12,
    fat16,
    fat32,
};

const Time = packed struct {
    created_second: u5 = 0,
    created_minute: u6 = 0,
    created_hour: u5 = 0,
};

const Date = packed struct {
    created_day: u5 = 0,
    created_month: u4 = 0,
    created_year: u7 = 0,
};

const File = extern struct {
    name: [8]u8 align(1),
    extension: [3]u8 align(1),
    attributes: u8 align(1),
    reserved_for_windowsNT: u8 align(1) = 0,
    deciseconds: u8 align(1) = 0,
    created_time: Time align(1) = .{},
    created_date: Date align(1) = .{},
    accessed_date: Date align(1) = .{},
    cluster_hi: u16 align(1),
    modified_time: Time align(1) = .{},
    modified_date: Date align(1) = .{},
    cluster_lo: u16 align(1),
    size: u32 align(1),
    fs: *Fs,

    const Self = @This();
    const Error = error{
        NotFound,
        InvalidPath,
    };

    pub fn cluster(self: Self, fs: *Fs) !Cluster {
        return try Cluster.new(fs, (@as(u32, self.cluster_hi) << 16) | @as(u32, self.cluster_lo));
    }

    pub fn open(self: *const Self, path: []const u8) !Self {
        const stem = pathutil.stem(path);
        if (stem.len > 8) {
            @panic("path name too long");
        }

        const ext = pathutil.extension(path)[1..];
        if (ext.len > 3) {
            @panic("extension too long");
        }

        var name = [_]u8{0x20} ** 8;
        var extension = [_]u8{0x20} ** 3;
        mem.copy(u8, &name, stem);
        mem.copy(u8, &extension, ext);

        var files = [_]File{undefined} ** 16;

        var clusters = try self.cluster(self.fs);

        while (true) {
            const sector = clusters.sector(self.fs);

            self.fs.partition.load(.{
                .sector_count = 1,
                .buffer = @ptrCast([*]u8, &files),
                .sector = sector,
            });

            for (files) |file| {
                if (file.name[0] == 0) {
                    return Error.NotFound;
                }

                if (file.name[0] == 0xE5) {
                    continue;
                }

                if (mem.eql(u8, &name, &file.name) and mem.eql(u8, &extension, &file.extension)) {
                    return .{
                        .name = file.name,
                        .extension = file.extension,
                        .attributes = file.attributes,
                        .reserved_for_windowsNT = file.reserved_for_windowsNT,
                        .deciseconds = file.deciseconds,
                        .created_time = file.created_time,
                        .created_date = file.created_date,
                        .accessed_date = file.accessed_date,
                        .cluster_hi = file.cluster_hi,
                        .modified_time = file.modified_time,
                        .modified_date = file.modified_date,
                        .cluster_lo = file.cluster_lo,
                        .size = file.size,
                        .fs = self.fs,
                    };
                }
            }

            clusters = try clusters.next(self.fs);
        }

        return Error.NotFound;
    }

    pub fn read(self: *const Self, buffer: []u8) !void {
        var offset: u32 = 0;
        var scratch = [_]u8{0} ** 512;
        var clusters = try self.cluster(self.fs);
        while (offset < self.size) {
            self.fs.partition.load(.{
                .sector_count = 1,
                .buffer = @ptrCast([*]u8, &scratch),
                .sector = clusters.sector(self.fs),
            });

            mem.copy(u8, buffer[offset .. offset + 512], &scratch);

            clusters = clusters.next(self.fs) catch |err| {
                if (err == Cluster.Error.EndOfChain) {
                    return;
                }
                return err;
            };
            offset += 512;
        }
    }
};

const Metadata = struct {
    name: [256]u8,
    attributes: u8,
};

pub const Parameters = extern struct {
    stub: [3]u8 align(1),
    oem_name: [8]u8 align(1),
    bytes_per_sector: u16 align(1),
    sectors_per_cluster: u8 align(1),
    reserved_sectors: u16 align(1),
    fat_count: u8 align(1),
    root_entry_count: u16 align(1),
    total_sectors16: u16 align(1),
    media_type: u8 align(1),
    table_size16: u16 align(1),
    sectors_per_track: u16 align(1),
    head_side_count: u16 align(1),
    hidden_sector_count: u32 align(1),
    total_sectors32: u32 align(1),
    extended: [54]u8 align(1),

    const Self = @This();

    pub fn extended32(self: *const Self) *align(1) const Extended32 {
        return @ptrCast(*align(1) const Extended32, &self.extended);
    }
};

const Extended32 = extern struct {
    table_size32: u32 align(1),
    flags: u16 align(1),
    version: u16 align(1),
    root_cluster: u32 align(1),
    info: u16 align(1),
    backup_bootsector_sector: u16 align(1),
    reserved_0: [12]u8 align(1),
    drive: u8 align(1),
    reserved_1: u8 align(1),
    boot_signature: u8 align(1),
    volume_id: u32 align(1),
    volume_label: [11]u8 align(1),
    fat_type_label: [8]u8 align(1),
};

pub fn from(partition: *Partition, parameters_addr: usize) Fs {
    const parameters = @intToPtr(*Parameters, parameters_addr);

    var total_sectors = parameters.total_sectors32;
    var fat_size = parameters.extended32().table_size32;

    var root_dir_sectors = (parameters.root_entry_count * 32 + parameters.bytes_per_sector - 1) / parameters.bytes_per_sector;
    var first_data_sector = parameters.reserved_sectors + (parameters.fat_count * fat_size);
    var first_fat_sector = parameters.reserved_sectors;
    var data_sectors = total_sectors - (parameters.reserved_sectors + parameters.fat_count * fat_size + root_dir_sectors);
    var total_clusters = data_sectors / parameters.sectors_per_cluster;

    var kind: Kind = .fat32;
    var first_root_cluster = parameters.extended32().root_cluster;

    term.print("FAT FS TYPE: {s}\r\n", .{@tagName(kind)});

    return .{
        .kind = kind,
        .fat_size = fat_size,
        .cluster_bit_used = 28,
        .cluster_bit_width = 32,
        .first_data_sector = first_data_sector,
        .first_fat_sector = first_fat_sector,
        .sectors_per_cluster = parameters.sectors_per_cluster,
        .bytes_per_sector = parameters.bytes_per_sector,
        .total_sectors = total_sectors,
        .data_sectors = data_sectors,
        .reserved_sectors = parameters.reserved_sectors,
        .total_clusters = total_clusters,
        .partition = partition,
        .first_root_cluster = first_root_cluster,
        .root_dir_sectors = root_dir_sectors,
    };
}

pub fn root(self: *Fs) File {
    return .{
        .name = .{ '/', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
        .attributes = 0x10,
        .extension = .{ ' ', ' ', ' ' },
        .cluster_hi = @truncate(u16, self.first_root_cluster >> 16),
        .cluster_lo = @truncate(u16, self.first_root_cluster),
        .size = self.root_dir_sectors * self.bytes_per_sector,
        .fs = self,
    };
}

fn cluster_mask(self: *const Fs) u32 {
    return (@as(u32, 1) << @truncate(u5, self.cluster_bit_used)) - 1;
}

pub const Cluster = struct {
    cluster: u32,

    const Self = @This();
    pub const Error = error{
        EndOfChain,
    };

    fn new(fs: *const Fs, cluster: u32) !Self {
        if (cluster >= 0xFFFFFFF8 & fs.cluster_mask()) {
            return Error.EndOfChain;
        }

        return .{ .cluster = cluster & ((@as(u32, 1) << @truncate(u5, fs.cluster_bit_used)) - 1) };
    }

    pub fn sector(self: *const Self, fs: *const Fs) u32 {
        return (self.cluster - 2) * fs.sectors_per_cluster + fs.first_data_sector;
    }

    pub fn next(self: *const Self, fs: *const Fs) !Self {
        var scratch = [_]u8{0} ** 512;
        var cluster = self.cluster;

        var fat_offset: u32 = cluster * 4;

        const next_sector = fs.first_fat_sector + (fat_offset / fs.bytes_per_sector);
        const offset = fat_offset % fs.bytes_per_sector;

        fs.partition.load(.{
            .sector_count = 1,
            .buffer = @ptrCast([*]u8, &scratch),
            .sector = next_sector,
        });

        const raw = @ptrCast([*]u8, &scratch) + offset;
        cluster = @ptrCast(*align(1) u32, raw).*;

        return try Self.new(fs, cluster);
    }
};
