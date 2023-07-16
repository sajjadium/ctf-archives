const std = @import("std");
const builtin = std.builtin;
const fs = std.fs;
const mem = std.mem;
const feature = std.Target.x86.Feature;

const CrossTarget = std.zig.CrossTarget;
const AssemblyStep = @import("steps/Assembler.zig");
const ExtendedStep = @import("steps/ExtendedBootloader.zig");
const ArrayList = std.ArrayList;
const Build = std.Build;
const Step = Build.Step;
const CompileStep = Build.CompileStep;
const FeatureSet = std.Target.Cpu.Feature.Set;

pub fn build(b: *Build) void {
    buildErr(b) catch |err| @panic(@errorName(err));
}

fn buildErr(b: *Build) !void {
    var add = FeatureSet.empty;
    var sub = FeatureSet.empty;
    add.addFeature(@enumToInt(feature.soft_float));
    sub.addFeature(@enumToInt(feature.mmx));
    sub.addFeature(@enumToInt(feature.sse));
    sub.addFeature(@enumToInt(feature.sse2));
    sub.addFeature(@enumToInt(feature.avx));
    sub.addFeature(@enumToInt(feature.avx2));

    const target16 = .{
        .cpu_arch = .x86,
        .os_tag = .freestanding,
        .abi = .code16,
        .cpu_features_add = add,
        .cpu_features_sub = sub,
    };

    const target64 = .{
        .cpu_arch = .x86_64,
        .os_tag = .freestanding,
        .abi = .none,
        .cpu_features_add = add,
        .cpu_features_sub = sub,
    };

    try buildBootModule(b, .{
        .name = "mbrsector",
        .path = "src/mbrsector",
        .target = target16,
        .optimize = .ReleaseSmall,
    });
    try buildBootModule(b, .{
        .name = "bootsector",
        .path = "src/bootsector",
        .target = target16,
        .optimize = .ReleaseSmall,
    });
    try buildBootModule(b, .{
        .name = "extended",
        .path = "src/extended",
        .target = target16,
        .optimize = .ReleaseSmall,
    });

    try buildDisk(b, .{
        .mbrsector = &.{
            "boot",
            "mbrsector.bin",
        },
        .bootsector = &.{
            "boot",
            "bootsector.bin",
        },
        .extended = &.{
            "boot",
            "extended.bin",
        },
    });

    const app = b.addExecutable(.{
        .name = "app",
        .root_source_file = .{
            .path = "src/main.zig",
        },
        .target = target64,
        .optimize = .ReleaseSmall,
    });
    app.addAssemblyFile("src/switch/code32.s");
    app.addAssemblyFile("src/switch/code64.s");
    app.addAssemblyFile("src/switch/interrupt.s");
    app.addAssemblyFile("src/switch/serial.s");
    app.setLinkerScriptPath(.{
        .path = "src/linker.ld",
    });
    app.install();

    installAt(b, flatBinary(b, app), "boot/app.bin");
}

fn buildDisk(b: *Build, options: struct {
    mbrsector: []const []const u8,
    bootsector: []const []const u8,
    extended: []const []const u8,
}) !void {
    const arena = b.allocator;
    //// negligible memory leak here
    const mbrsector = b.getInstallPath(.prefix, try fs.path.join(arena, options.mbrsector));
    const bootsector = b.getInstallPath(.prefix, try fs.path.join(arena, options.bootsector));
    const extended = b.getInstallPath(.prefix, try fs.path.join(arena, options.extended));

    const create_disk = b.addSystemCommand(&.{
        "dd", "if=/dev/zero", "of=disk.img", "bs=1K", "count=512",
    });
    const create_partition_table = b.addSystemCommand(&.{
        "mpartition", "-I", "-B", mbrsector, "C:",
    });
    const create_partition = b.addSystemCommand(&.{
        "mpartition", "-c", "-a", "C:",
    });
    const format_partition = b.addSystemCommand(&.{
        "mformat", "-F", "-R", "64", "-B", bootsector, "C:",
    });
    const add_extended_bootloader = ExtendedStep.create(b, .{
        .disk_image = .{
            .path = "disk.img",
        },
        .extended_bootloader = .{
            .path = extended,
        },
    });
    const add_file = b.addSystemCommand(&.{ "mcopy", "zig-out/boot/app.bin", "C:" });
    const add_flag = b.addSystemCommand(&.{ "mcopy", "flag.txt", "C:" });

    const step = b.step("disk", "build disk");
    create_partition_table.step.dependOn(&create_disk.step);
    create_partition_table.step.dependOn(b.getInstallStep());
    create_partition.step.dependOn(&create_partition_table.step);
    format_partition.step.dependOn(&create_partition.step);
    add_extended_bootloader.step.dependOn(&format_partition.step);
    add_file.step.dependOn(&add_extended_bootloader.step);
    add_flag.step.dependOn(&add_file.step);
    step.dependOn(&add_flag.step);
}

const BuildOptions = struct {
    name: []const u8,
    path: []const u8,
    target: CrossTarget,
    optimize: builtin.OptimizeMode = .Debug,
};

fn buildBootModule(b: *Build, options: BuildOptions) !void {
    const elf = try buildModule(b, options);
    const dst = try fs.path.join(b.allocator, &.{
        "boot",
        b.fmt("{s}.bin", .{
            options.name,
        }),
    });
    installAt(b, flatBinary(b, elf), dst);
}

fn installAt(b: *Build, bin: anytype, path: []const u8) void {
    b.getInstallStep().dependOn(&b.addInstallFile(bin.getOutputSource(), path).step);
}

fn flatBinary(b: *Build, elf: *CompileStep) *Build.ObjCopyStep {
    return b.addObjCopy(elf.getOutputSource(), .{ .format = .bin });
}

fn buildModule(b: *Build, options: BuildOptions) !*CompileStep {
    const arena = b.allocator;
    const common = try files(arena, "src/common", .{});
    const assembly = try files(arena, options.path, .{});

    const main = try fs.path.join(arena, &.{
        options.path,
        "main.zig",
    });
    const linker_script = try fs.path.join(arena, &.{
        options.path,
        "linker.ld",
    });

    const elf = b.addExecutable(.{
        .name = options.name,
        .root_source_file = .{
            .path = main,
        },
        .target = options.target,
        .optimize = options.optimize,
    });
    elf.setLinkerScriptPath(.{
        .path = linker_script,
    });

    for (assembly.items) |path| {
        if (isExtention(path, ".s")) {
            elf.addAssemblyFile(path);
        }
    }

    for (common.items) |path| {
        if (isExtention(path, ".zig")) {
            const name = fs.path.stem(path);
            elf.addAnonymousModule(name, .{
                .source_file = .{
                    .path = path,
                },
            });
        }
    }

    elf.install();

    return elf;
}

fn isExtention(path: []const u8, extension: []const u8) bool {
    return mem.eql(u8, extension, fs.path.extension(path));
}

fn files(arena: anytype, path: []const u8, options: struct {
    recursive: bool = true,
}) !ArrayList([]const u8) {
    var file_list = ArrayList([]const u8).init(arena);

    var directory = try fs.cwd().openIterableDir(path, .{});
    defer directory.close();

    var it = directory.iterate();
    while (try it.next()) |entry| {
        switch (entry.kind) {
            .File => {
                const file_path = try fs.path.join(arena, &[_][]const u8{
                    path,
                    entry.name,
                });
                try file_list.append(file_path);
            },
            .Directory => {
                const directory_path = try fs.path.join(arena, &[_][]const u8{
                    path,
                    entry.name,
                });
                const recursive = try files(arena, directory_path, options);
                try file_list.appendSlice(recursive.items);
                recursive.deinit();
                arena.free(directory_path);
            },
            else => {},
        }
    }

    return file_list;
}
