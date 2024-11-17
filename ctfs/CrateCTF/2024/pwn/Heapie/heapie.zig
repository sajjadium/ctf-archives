// $ zig version
// 0.13.0
// $ zig build-exe -target x86_64-linux -OReleaseSafe -fstrip heapie.zig

const std = @import("std");
const builtin = @import("builtin");

pub fn main() !void {
    const flag = try std.fs.cwd().openFile("flag.txt", .{});
    const mem = try std.posix.mmap(
        null,
        std.mem.page_size,
        std.posix.PROT.READ | std.posix.PROT.WRITE,
        .{ .TYPE = .PRIVATE, .ANONYMOUS = false },
        flag.handle,
        0,
    );
    flag.close();
    defer std.posix.munmap(mem);

    var gpa = std.heap.GeneralPurposeAllocator(.{}){ .backing_allocator = std.heap.page_allocator };
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Just testing to see if the allocator is working. Don't mind this :))))
    var slices: [11][]u8 = undefined;
    inline for (0.., &slices) |i, *s| s.* = try allocator.alloc(u8, 1 << i);
    defer for (slices) |s| allocator.free(s);

    var state = State.init(allocator);

    while (true) {
        const line = try state.prompt(
            \\Options:
            \\  - np: new paragraph
            \\  - gp: get paragraph
            \\  - sp: set paragraph
            \\  - rp: remove paragraph
            \\
            \\  - cd: create document
            \\  - gd: get document
            \\  - rd: remove document
            \\  - e: exit
        ,
            .{},
        ) orelse break;

        const Opts = enum { np, gp, sp, rp, cd, gd, rd, e };
        const opt = std.meta.stringToEnum(Opts, line) orelse continue;
        (switch (opt) {
            .np => state.newParagraph(),
            .gp => state.getParagraph(),
            .sp => state.setParagraph(),
            .rp => state.removeParagraph(),

            .cd => state.createDocument(),
            .gd => state.getDocument(),
            .rd => state.removeDocument(),
            .e => break,
        }) catch |err| if (err == error.BadInput) {
            try state.stdout.print(">:(\n", .{});
        } else return err;
    }
}

const State = struct {
    paragraphs: std.StringHashMapUnmanaged([]u8),
    documents: std.StringHashMapUnmanaged([][]u8),

    allocator: std.mem.Allocator,
    stdout: std.fs.File.Writer,
    stdin: std.fs.File.Reader,
    current_line: std.ArrayListUnmanaged(u8),

    const Self = @This();

    fn init(allocator: std.mem.Allocator) Self {
        return .{
            .paragraphs = .{},
            .documents = .{},

            .allocator = allocator,
            .stdout = std.io.getStdOut().writer(),
            .stdin = std.io.getStdIn().reader(),
            .current_line = .{},
        };
    }

    fn prompt(self: *Self, comptime fmt: []const u8, args: anytype) !?[]u8 {
        try self.stdout.print(fmt ++ "\n> ", args);
        self.current_line.clearRetainingCapacity();
        self.stdin.streamUntilDelimiter(self.current_line.writer(self.allocator), '\n', null) catch |err| switch (err) {
            error.EndOfStream => return null,
            else => return err,
        };
        return self.current_line.items;
    }

    fn newParagraph(self: *Self) !void {
        const name = try self.allocator.dupe(u8, try self.prompt("Name", .{}) orelse return error.BadInput);
        const len_string = try self.prompt("Length", .{}) orelse return error.BadInput;
        const len = std.fmt.parseInt(u11, len_string, 10) catch return error.BadInput;
        try self.paragraphs.put(self.allocator, name, try self.allocator.alloc(u8, len));
    }

    fn getParagraph(self: *Self) !void {
        const name = try self.prompt("Name", .{}) orelse return error.BadInput;
        const paragraph = self.paragraphs.get(name);
        try self.stdout.print("{?s}\n", .{paragraph});
    }

    fn setParagraph(self: *Self) !void {
        const name = try self.prompt("Name", .{}) orelse return error.BadInput;
        const contents = self.paragraphs.get(name) orelse return error.BadInput;
        const paragraph = try self.prompt("Contents", .{}) orelse return error.BadInput;
        if (contents.len != paragraph.len) return error.BadInput;
        @memcpy(contents, paragraph);
    }

    fn removeParagraph(self: *Self) !void {
        const name = try self.prompt("Name", .{}) orelse return error.BadInput;
        const paragraph = self.paragraphs.get(name) orelse return error.BadInput;
        self.allocator.free(paragraph);
    }

    fn createDocument(self: *Self) !void {
        const name = try self.allocator.dupe(u8, try self.prompt("Name", .{}) orelse return error.BadInput);
        const count_string = try self.prompt("Paragraph count", .{}) orelse return error.BadInput;
        const count = std.fmt.parseInt(u7, count_string, 10) catch return error.BadInput;
        const document = try self.allocator.alloc([]u8, count);
        errdefer self.allocator.free(document);
        for (document) |*par| {
            const par_name = try self.prompt("Paragraph name", .{}) orelse return error.BadInput;
            par.* = self.paragraphs.get(par_name) orelse return error.BadInput;
        }
        try self.documents.put(self.allocator, name, document);
    }

    fn getDocument(self: *Self) !void {
        const name = try self.prompt("Name", .{}) orelse return error.BadInput;
        const document = self.documents.get(name) orelse return error.BadInput;

        for (0.., document) |i, paragraph| {
            try self.stdout.print("{s}{}: {s}\n", .{ if (i > 0) "\n" else "", i, paragraph });
        }
    }

    fn removeDocument(self: *Self) !void {
        const name = try self.prompt("Name", .{}) orelse return error.BadInput;
        const document = self.documents.get(name) orelse return error.BadInput;
        self.allocator.free(document);
    }
};
