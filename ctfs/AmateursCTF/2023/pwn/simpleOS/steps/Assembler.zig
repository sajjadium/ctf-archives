const std = @import("std");
const Assembler = @This();
const Build = std.Build;
const Builder = Build.Builder;
const FileSource = Build.FileSource;
const GeneratedFile = Build.GeneratedFile;
const CrossTarget = std.zig.CrossTarget;
const Step = Build.Step;
const Arch = std.Target.Cpu.Arch;

const fs = std.fs;

const Options = struct {
    source_file: FileSource,
    name: []const u8,
    cpu_arch: ?Arch,
};

step: Step,
source_file: FileSource,
cpu_arch: ?Arch,
output_name: []const u8,
output_file: GeneratedFile,

const Self = @This();
pub const base_id: Step.Id = .custom;

pub fn create(owner: *Builder, options: Options) *Self {
    const self = owner.allocator.create(Self) catch @panic("OOM");
    const step = Step.init(.{
        .id = base_id,
        .name = owner.fmt("assemble {s}", .{options.source_file.path}),
        .owner = owner,
        .makeFn = make,
    });

    self.* = Self{
        .step = step,
        .source_file = options.source_file,
        .cpu_arch = options.cpu_arch,
        .output_name = owner.fmt("{s}.o", .{options.name}),
        .output_file = .{
            .step = &self.step,
        },
    };
    return self;
}

pub fn getOutputSource(self: *const Self) FileSource {
    return .{
        .generated = &self.output_file,
    };
}

fn make(step: *Step, progress: *std.Progress.Node) !void {
    _ = progress;

    const builder = step.owner;
    const self = @fieldParentPtr(Self, "step", step);

    var man = builder.cache.obtain();
    defer man.deinit();

    man.hash.add(@as(u32, 0xfadefade));

    const full_src_path = self.source_file.getPath(builder);
    _ = try man.addFile(full_src_path, null);

    _ = try step.cacheHit(&man);

    const digest = man.final();
    const full_dest_path = builder.cache_root.join(builder.allocator, &.{
        "o", &digest, self.output_name,
    }) catch unreachable;
    const cache_path = "o" ++ fs.path.sep_str ++ &digest;
    builder.cache_root.handle.makePath(cache_path) catch |err| {
        return step.fail("unable to make path {s}: {s}", .{ cache_path, @errorName(err) });
    };

    self.output_file.path = full_dest_path;

    const argv = [_][]const u8{
        "as",
        "-o",
        full_dest_path,
        full_src_path,
    };

    try Step.evalChildProcess(step, &argv);
}
