const std = @import("std");
const disk = @import("disk.zig");
const term = @import("term.zig");
const fs = @import("extended/fs.zig");
const mem = std.mem;
const Allocator = mem.Allocator;
const Parameters = fs.Parameters;

var parameters: Parameters = undefined;
var relative: usize = undefined;
var manager: Allocator = undefined;
var files: std.StringHashMap(*File) = undefined;

pub fn init(allocator: Allocator) void {
    parameters = @intToPtr(*Parameters, 0x7C00).*;

    var total_sectors = @as(u32, parameters.total_sectors16);
    if (total_sectors == 0) {
        total_sectors = parameters.total_sectors32;
    }
    var fat_size = parameters.extended32().table_size32;

    var first_data_sector = parameters.reserved_sectors + (parameters.fat_count * fat_size);
    var data_sectors = total_sectors - (parameters.reserved_sectors + parameters.fat_count * fat_size);

    relative = first_data_sector + data_sectors;
    manager = allocator;
    files = std.StringHashMap(*File).init(allocator);

    term.printf("first availible sector: {}\r\n", .{relative});
}

pub fn new(name: []const u8, size: usize) !*File {
    var file = try manager.create(File);
    try file.init(name, size);
    try files.put(name, file);
    return file;
}

pub fn open(name: []const u8) !*File {
    var file = files.get(name) orelse {
        term.printf("file `{s}` does not exist\r\n", .{name});
        return std.os.AcceptError.FileNotFound;
    };
    return file;
}

pub const File = struct {
    name: []const u8,
    cache: [512]u8,
    sector: usize,
    size: usize,
    offset: usize,

    const Self = @This();

    pub fn init(self: *Self, name: []const u8, size: usize) !void {
        const sectors = (size + 511 & ~@as(usize, 511)) / 512;

        defer self.name = name;
        self.sector = relative;
        self.size = size;
        self.offset = 0;

        try disk.read(self.sector, self.view());
        relative += sectors;
    }

    fn die(err: anyerror) void {
        term.printf("disk error: {s}\r\n", .{@errorName(err)});
    }

    pub fn write(self: *Self, buffer: []u8) !void {
        if (self.offset + buffer.len >= self.size) {
            return std.os.AccessError.InputTooLong;
        }

        var result = self.offset + buffer.len;
        defer self.offset = result;
        defer self.reload() catch |err| die(err);

        try disk.write(self.sector + self.offset / 512, @ptrCast([*]align(1) u16, buffer)[0 .. buffer.len / 2]);
    }

    pub fn seek(self: *Self, offset: usize) !void {
        if (offset >= self.size) {
            return std.os.AccessError.InputTooLong;
        }
        self.offset = offset;
        try self.reload();
    }

    pub fn peek(self: *Self) u8 {
        if (self.offset >= self.size) {
            return 0;
        }

        const ch = self.cache[self.offset % 512];
        return ch;
    }

    pub fn getchar(self: *Self) u8 {
        if (self.offset >= self.size) {
            return 0;
        }

        const ch = self.cache[self.offset % 512];
        self.offset += 1;
        if (self.offset % 512 == 0) {
            self.reload() catch |err| die(err);
        }
        return ch;
    }

    pub fn putback(self: *Self, ch: u8) void {
        _ = ch;
        if (self.offset > 0) {
            self.offset -= 1;
        }
        if (self.offset % 512 == 511) {
            self.reload() catch |err| die(err);
        }
    }

    fn view(self: *Self) []align(1) u16 {
        return @ptrCast([*]align(1) u16, &self.cache)[0..256];
    }

    fn reload(self: *Self) !void {
        try disk.read(self.sector + self.offset / 512, self.view());
    }
};
