const std = @import("std");
const term = @import("term.zig");
const arch = @import("arch.zig");
const pio = @import("pio.zig");
const fs = @import("fs.zig");
const disk = @import("disk.zig");
const ascii = std.ascii;
const mem = std.mem;
const fmt = std.fmt;
const math = std.math;
const ArrayList = std.ArrayList;

pub const Error = error{
    MissingStartBlock,
    MissingEndBlock,
    UnexpectedCharacter,
    UndefinedVariable,
    InvalidChoice,
};

const Variables = std.StringHashMap(isize);
pub const Environment = struct {
    variables: Variables,
    chain: ?*Environment,
    depth: usize,

    const Self = @This();

    pub fn get(self: *Self, name: []const u8) ?isize {
        if (self.variables.get(name)) |v| {
            return v;
        }
        if (self.chain) |next| {
            return next.get(name);
        }
        return null;
    }

    fn put(self: *Self, name: []const u8, v: isize) !void {
        var env: *Environment = self;
        while (env.depth != 0) : (env = env.chain.?) {
            if (env.variables.getPtr(name)) |ptr| {
                ptr.* = v;
                return;
            }
        }
        try env.variables.put(name, v);
    }

    fn nest(self: *Self, allocator: anytype) Self {
        return .{
            .variables = Variables.init(allocator),
            .chain = self,
            .depth = self.depth + 1,
        };
    }

    fn deinit(self: *Self, allocator: anytype) void {
        var it = self.variables.keyIterator();
        while (it.next()) |key| {
            allocator.free(key.*);
        }
        self.variables.deinit();
    }
};

pub noinline fn start(allocator: anytype) void {
    var env = Environment{
        .variables = Variables.init(allocator),
        .chain = undefined,
        .depth = 0,
    };
    env.put("flag", 0xfaaf) catch |err| {
        term.printf("error: {s}\r\n", .{@errorName(err)});
        @panic("fatal error");
    };

    var stdin = Stream{
        .term = {},
    };

    while (true) {
        loop(stdin, &env, allocator) catch |err| {
            term.printf("error: {s}\n", .{@errorName(err)});
            term.flush();
        };
    }
}

var tmp: *fs.File = undefined;

fn loop(stream: anytype, env: *Environment, allocator: anytype) !void {
    term.printf(
        \\
        \\0. print flag variable
        \\1. input program
        \\2. echo on
        \\3. echo off
        \\4. exec file
        \\5. open file
        \\6. seek file
        \\7. make file
        \\8. write file
        \\
    , .{});
    stream.ignore(ascii.isWhitespace);
    const choice = try stream.readnum(allocator);
    term.printf("you chose option #{}\r\n", .{choice});
    switch (choice) {
        0 => term.printf("flag: {?}\r\n", .{env.get("flag")}),
        1 => {
            term.printf("gimme code now\r\n", .{});
            stream.ignore(ascii.isWhitespace);
            try stream.expect(char('{'));
            try run(stream, allocator, env);
        },
        2 => {
            term.echo(true);
            term.printf("echo on\r\n", .{});
        },
        3 => {
            term.echo(false);
            term.printf("echo off\r\n", .{});
        },
        4 => {
            var input = Stream{
                .file = tmp,
            };
            try input.expect(char('{'));
            try run(input, allocator, env);
        },
        5 => {
            term.printf("name: ", .{});
            var name = try stream.read(allocator, not(newline));
            defer name.deinit();
            errdefer name.deinit();
            try stream.expect(newline);
            tmp = try fs.open(name.items);
        },
        6 => {
            term.printf("offset: ", .{});
            const offset = try stream.readnum(allocator);
            try tmp.seek(offset);
        },
        7 => {
            term.printf("name: ", .{});
            var name = try stream.read(allocator, not(newline));
            defer name.deinit();
            errdefer name.deinit();
            try stream.expect(newline);
            term.printf("size: ", .{});
            var size = try stream.readnum(allocator);
            tmp = try fs.new(name.items, size);
        },
        8 => {
            term.printf("size: ", .{});
            var size = try stream.readnum(allocator);
            var data = try allocator.alloc(u8, size);
            defer allocator.free(data);
            errdefer allocator.free(data);
            term.printf("data: ", .{});
            for (0..size) |i| {
                data[i] = stream.getchar();
            }
            try stream.expect(newline);
            try tmp.write(data);
        },
        else => return Error.InvalidChoice,
    }
}

fn identifier(ch: u8) bool {
    return !ascii.isWhitespace(ch) and (ascii.isAlphanumeric(ch) or oneof(ch, "_"));
}

fn oneof(needle: u8, haystack: []const u8) bool {
    if (mem.indexOfScalar(u8, haystack, needle)) |_| {
        return true;
    } else {
        return false;
    }
}

fn newline(ch: u8) bool {
    return ch == '\n' or ch == '\r';
}

fn not(comptime rule: Rule) Rule {
    const Inverse = struct {
        fn fun(ch: u8) bool {
            return !rule(ch);
        }
    };
    return Inverse.fun;
}

fn char(comptime ch: u8) Rule {
    const Char = struct {
        fn fun(a: u8) bool {
            return ch == a;
        }
    };
    return Char.fun;
}

pub const Rule = *const fn (ch: u8) bool;

pub const Stream = union(enum) {
    term: void,
    file: *fs.File,

    const Self = @This();

    pub fn readnum(self: Self, allocator: mem.Allocator) !usize {
        var buf = try self.read(allocator, not(newline));
        defer buf.deinit();
        errdefer buf.deinit();
        const res = try fmt.parseInt(usize, buf.items, 10);
        try self.expect(newline);
        return res;
    }

    pub fn getchar(self: Self) u8 {
        return switch (self) {
            .term => term.getchar(),
            .file => |f| f.getchar(),
        };
    }

    pub fn putback(self: Self, ch: u8) void {
        switch (self) {
            .term => term.putback(ch),
            .file => |f| f.putback(ch),
        }
    }

    pub fn peek(self: Self) u8 {
        return switch (self) {
            .term => term.peek(),
            .file => |f| f.peek(),
        };
    }

    pub fn expect(self: Self, rule: Rule) Error!void {
        const ch = self.getchar();
        if (!rule(ch)) {
            term.printf("unexpected character, found `{c}`\r\n", .{ch});
            return Error.UnexpectedCharacter;
        }
    }

    const String = ArrayList(u8);

    pub fn read(self: Self, allocator: mem.Allocator, rule: Rule) !String {
        var string = String.init(allocator);
        var ch = self.getchar();
        while (rule(ch)) : (ch = self.getchar()) {
            try string.append(ch);
        }
        self.putback(ch);
        return string;
    }

    pub fn ignore(self: Self, rule: Rule) void {
        var ch = self.getchar();
        while (rule(ch)) : (ch = self.getchar()) {}
        self.putback(ch);
    }

    pub fn optional(self: Self, haystack: []const u8) ?u8 {
        const needle = self.peek();
        if (oneof(needle, haystack)) {
            _ = self.getchar();
            return needle;
        } else {
            return null;
        }
    }

    pub fn value(self: Self, allocator: anytype, env: *Environment) !isize {
        const next = self.peek();
        if (ascii.isDigit(next) or next == '-') {
            var negative: isize = 1;
            if (next == '-') {
                negative = -1;
                _ = self.getchar();
            }
            const number = try self.read(allocator, ascii.isDigit);
            defer number.deinit();
            return negative * try fmt.parseInt(isize, number.items, 10);
        } else {
            const ident = try self.read(allocator, identifier);
            defer ident.deinit();
            if (env.get(ident.items)) |v| {
                return v;
            }
            term.printf("could not find variable `{s}`\r\n", .{ident.items});
            return Error.UndefinedVariable;
        }
    }
};

fn run(stream: Stream, allocator: mem.Allocator, env: *Environment) !void {
    var nest = env.nest(allocator);
    defer nest.deinit(allocator);
    errdefer nest.deinit(allocator);

    while (true) {
        const next = stream.getchar();
        switch (next) {
            '\r', '\n', ' ', '\t' => continue,
            '}' => break,
            '{' => {
                try run(stream, allocator, &nest);
            },
            else => {
                stream.putback(next);
                const ident = try stream.read(allocator, identifier);
                stream.ignore(ascii.isWhitespace);
                try stream.expect(char('='));
                stream.ignore(ascii.isWhitespace);
                var num = try stream.value(allocator, &nest);
                stream.ignore(ascii.isWhitespace);
                if (stream.optional("-+/*")) |op| {
                    stream.ignore(ascii.isWhitespace);
                    var rhs = try stream.value(allocator, &nest);
                    switch (op) {
                        '-' => num -= rhs,
                        '+' => num += rhs,
                        '/' => {
                            num = try math.divTrunc(isize, num, rhs);
                        },
                        '*' => num *= rhs,
                        else => unreachable,
                    }
                }
                try stream.expect(char(';'));
                try nest.put(ident.items, num);
            },
        }
    }
}
