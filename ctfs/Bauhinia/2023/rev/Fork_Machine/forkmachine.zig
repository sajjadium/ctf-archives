const std = @import("std");
const builtin = @import("builtin");


// Requirements
comptime {
    std.debug.assert(builtin.os.tag == .linux);
    std.debug.assert(!builtin.single_threaded);
    // Zig version 0.11.0-dev.4234+dc2483516
    // Works on Linux only. There are modifications that need to be made for this to work:
    // - Modify std/heap/PageAllocator.zig such that MAP_SHARED is used instead of MAP_PRIVATE
    // - Modify std/Thread/Futex.zig such that both occurences of the PRIVATE flag is removed
    // - Workaround a Zig bug: Remove the usage of tls_thread_id variable in LinuxThreadImpl struct in std/Thread.zig
    //              I guess they forgot to update that variable when fork() is called.
}

pub fn setPdeathsig() void {
    _ = std.os.prctl(.SET_PDEATHSIG, .{std.os.SIG.KILL}) catch unreachable;
}

pub fn waitAllChildren() void {
    var status: u32 = undefined;
    while (true) {
        const rc = std.os.system.waitpid(-1, &status, 0);
        switch (std.os.errno(rc)) {
            .SUCCESS => continue,
            .INTR => continue,
            .CHILD => return,
            .INVAL => unreachable, // Invalid flags.
            else => unreachable,
        }
    }
}

const IPC_Event = struct {
    fired: bool = false,
    mutex: std.Thread.Mutex = .{},
    condition: std.Thread.Condition = .{},

    pub fn wait(self: *@This()) void {
        self.mutex.lock();
        defer self.mutex.unlock();

        while (!self.fired) {
            self.condition.wait(&self.mutex);
        }
    }

    pub fn signal(self: *@This()) void {
        self.mutex.lock();
        defer self.mutex.unlock();

        std.debug.assert(!self.fired);
        self.fired = true;
        self.condition.broadcast();
    }
};


const SharedGlobals = struct {
    const MAX_NUM_VMNODES = 1_000_000;
    const MAX_DYNAMIC_ALLOC_BYTES = 1_000_000;
    fba_buf: [MAX_DYNAMIC_ALLOC_BYTES]u8,
    fba: std.heap.FixedBufferAllocator,
    allocator: std.mem.Allocator,
    nodes: [MAX_NUM_VMNODES]VMNode,
    next_instance_base: u64,
    instancing_mutex: std.Thread.Mutex,
    scope_templates: []ScopeTemplate,
};
var SHARED_GLOBALS: *SharedGlobals = undefined;

pub fn getNode(idx: u64) *VMNode {
    return &SHARED_GLOBALS.nodes[idx];
}


const ValueType = enum {
    int,
    vector,
};
const VMNodeType = enum {
    constant,
    vector,
    compute,
    phi,
    phi_setter,
    scope_instantiator,
};
const ComputeOpType = enum {
    add,
    sub,
    mul,
    div,
    mod,
    and_,
    or_,
    xor,
    boolean_not,
    boolean_and,
    boolean_or,
    equal,
    less,
    less_equal,
    greater,
    greater_equal,
    // Vector values only
    get_size,
    get_at_index,
    copy_with_set_at_index,
};


const Value = union(ValueType) {
    int: i64,
    vector: []Value,
    pub fn equal(self: @This(), other: @This()) bool {
        if (@intFromEnum(self) != @intFromEnum(other)) return false;
        switch (self) {
            .int => return self.int == other.int,
            .vector => {
                if (self.vector.len != other.vector.len) return false;
                for (self.vector, other.vector) |value1, value2| {
                    if (!value1.equal(value2)) return false;
                }
                return true;
            }
        }
    }
    pub fn shalow_copy(self: @This()) !@This() {
        switch (self) {
            .int => return @This(){.int = self.int},
            .vector => {
                var ret = @This(){.vector = try SHARED_GLOBALS.allocator.alloc(@This(), self.vector.len)};
                for (0..self.vector.len) |i| {
                    ret.vector[i] = self.vector[i];
                }
                return ret;
            }
        }
    }
    pub fn print(self: @This()) void {
        switch (self) {
            .int => std.debug.print("{}", .{self.int}),
            .vector => {
                std.debug.print("[", .{});
                for (self.vector, 0..) |item, i| {
                    if (i > 0) std.debug.print(", ", .{});
                    item.print();
                }
                std.debug.print("]", .{});
            }
        }
    }
    pub fn print_string(self: @This()) void {
        switch (self) {
            .int => unreachable,
            .vector => {
                for (self.vector) |item| {
                    if (item != .int) {
                        unreachable;
                    } else if (item.int >= 32 and item.int <= 127) {
                        std.debug.print("{c}", .{@as(u8, @truncate(@as(u64, @bitCast(item.int))))});
                    } else {
                        std.debug.print("\\{d}", .{@as(u8, @truncate(@as(u64, @bitCast(item.int))))});
                    }
                }
            }
        }
    }
};


const VMNode = struct {
    node_type: VMNodeType,
    instance_id_base: u64 = undefined,
    id: u32,
    ipcev_instancing_done: *IPC_Event = undefined,
    requirements: []u32,
    value: Value = undefined,
    ipcev_done: IPC_Event = .{},

    // Constant
    constant_value: Value = undefined,

    // Compute
    op: ComputeOpType = undefined,
    operand_id_1: ?u32 = null,
    operand_id_2: ?u32 = null,
    operand_id_3: ?u32 = null,

    // Vector
    vector_element_ids: []u32 = undefined,

    // Phi
    ipcev_is_set: IPC_Event = .{},
    absolute_source_id: u64 = undefined,

    // Phi Setter
    phi_setter_absolute_source_id: u64 = undefined,
    phi_setter_absolute_destination_id: u64 = undefined,
    phi_setter_source_id: u32 = undefined,
    phi_setter_destination_id: u32 = undefined,
    phi_setter_destination_up: u32 = undefined,

    // Scope Instantiator
    scope_template_index: u32 = undefined,
    scope_args: []u32 = undefined,
    scope_iteration: u32 = 0,
    scope_loop_root: u64 = 0,

    pub fn process(self: *@This()) !void {
        self.ipcev_instancing_done.wait();
        for (self.requirements) |requirement_id| {
            var requirement_node = getNode(self.instance_id_base + requirement_id);
            requirement_node.ipcev_done.wait();
            if (requirement_node.value.equal(.{.int = 0})) {
                return;
            }
        }
        switch (self.node_type) {
            .constant => self.value = self.constant_value,
            .compute => {
                var num_operands: u32 = 0;
                var operand1: *VMNode = undefined;
                var operand2: *VMNode = undefined;
                var operand3: *VMNode = undefined;
                if (self.operand_id_1) |operand_id_1| {
                    operand1 = getNode(self.instance_id_base + operand_id_1);
                    operand1.ipcev_done.wait();
                    num_operands += 1;
                }
                if (self.operand_id_2) |operand_id_2| {
                    operand2 = getNode(self.instance_id_base + operand_id_2);
                    operand2.ipcev_done.wait();
                    num_operands += 1;
                }
                if (self.operand_id_3) |operand_id_3| {
                    operand3 = getNode(self.instance_id_base + operand_id_3);
                    operand3.ipcev_done.wait();
                    num_operands += 1;
                }
                switch (num_operands) {
                    0 => unreachable,
                    1 => switch (self.op) {
                        .boolean_not => {
                            if (operand1.value != .int) unreachable;
                            self.value = Value {.int = @intFromBool(operand1.value.int == 0)};
                        },
                        .get_size => {
                            if (operand1.value != .vector) unreachable;
                            self.value = Value {.int = @as(i64, @bitCast(operand1.value.vector.len))};
                        },
                        else => unreachable
                    },
                    2 => {
                        if (operand1.value == .int and operand2.value == .int) {
                            var A: i64 = operand1.value.int;
                            var B: i64 = operand2.value.int;
                            var RES: i64 = undefined;
                            switch (self.op) {
                                .add => RES = A + B,
                                .sub => RES = A - B,
                                .mul => RES = A * B,
                                .div => RES = @divFloor(A, B),
                                .mod => RES = @mod(A, B),
                                .and_ => RES = A & B,
                                .or_ => RES = A | B,
                                .xor => RES = A ^ B,
                                .boolean_and => RES = @intFromBool(A != 0 and B != 0),
                                .boolean_or => RES = @intFromBool(A != 0 or B != 0),
                                .equal => RES = @intFromBool(A == B),
                                .less => RES = @intFromBool(A < B),
                                .less_equal => RES = @intFromBool(A <= B),
                                .greater => RES = @intFromBool(A > B),
                                .greater_equal => RES = @intFromBool(A >= B),
                                else => unreachable
                            }
                            self.value = Value {.int = RES};
                        } else {
                            switch (self.op) {
                                .mul => {
                                    if (operand1.value != .int and operand2.value != .int) unreachable;
                                    if (operand1.value == .int) {
                                        var t: *VMNode = operand1;
                                        operand1 = operand2;
                                        operand2 = t;
                                    }
                                    if (operand2.value.int < 0) unreachable;
                                    var times = @as(u64, @bitCast(operand2.value.int));
                                    var res_vector = try SHARED_GLOBALS.allocator.alloc(Value, operand1.value.vector.len * times);
                                    for (0..times) |i| {
                                        for (0..operand1.value.vector.len) |j| {
                                            res_vector[i * operand1.value.vector.len + j] = operand1.value.vector[j];
                                        }
                                    }
                                    self.value = Value {.vector = res_vector};
                                },
                                .add => {
                                    if (operand1.value != .vector or operand2.value != .vector) unreachable;
                                    var res_vector = try SHARED_GLOBALS.allocator.alloc(Value, operand1.value.vector.len + operand2.value.vector.len);
                                    for (0..operand1.value.vector.len) |i| {
                                        res_vector[i] = operand1.value.vector[i];
                                    }
                                    for (0..operand2.value.vector.len) |i| {
                                        res_vector[operand1.value.vector.len + i] = operand2.value.vector[i];
                                    }
                                    self.value = Value {.vector = res_vector};
                                },
                                .equal => {
                                    self.value = Value {.int = @intFromBool(operand1.value.equal(operand2.value))};
                                },
                                .get_at_index => {
                                    if (operand1.value != .vector or operand2.value != .int) unreachable;
                                    var index: i64 = operand2.value.int;
                                    if (index < 0) index += @as(i64, @bitCast(operand1.value.vector.len));
                                    if (index < 0 or index >= operand1.value.vector.len) unreachable;
                                    var unsigned_index = @as(u64, @bitCast(index));
                                    self.value = operand1.value.vector[unsigned_index];
                                },
                                else => unreachable
                            }
                        }
                    },
                    3 => {
                        switch (self.op) {
                            .copy_with_set_at_index => {
                                if (operand1.value != .vector or operand2.value != .vector) unreachable;

                                self.value = try operand1.value.shalow_copy();
                                var cur: Value = self.value;
                                for (0..operand2.value.vector.len) |i| {
                                    var index_value: Value = operand2.value.vector[i];
                                    if (index_value != .int) unreachable;
                                    var index = index_value.int;
                                    if (index < 0) index += @as(i64, @bitCast(cur.vector.len));
                                    if (index < 0 or index >= cur.vector.len) unreachable;
                                    var unsigned_index = @as(u64, @bitCast(index));
                                    if (i == operand2.value.vector.len - 1) {
                                        cur.vector[unsigned_index] = operand3.value;
                                    } else {
                                        cur.vector[unsigned_index] = try cur.vector[unsigned_index].shalow_copy();
                                        cur = cur.vector[unsigned_index];
                                        if (cur != .vector) unreachable;
                                    }
                                }
                            },
                            else => unreachable
                        }
                    },
                    else => unreachable,
                }
            },
            .vector => {
                var vector = try SHARED_GLOBALS.allocator.alloc(Value, self.vector_element_ids.len);
                for (self.vector_element_ids, 0..) |element_id, i| {
                    var element: *VMNode = getNode(self.instance_id_base + element_id);
                    element.ipcev_done.wait();
                    vector[i] = element.value;
                }
                self.value = Value {.vector = vector};
            },
            .phi => {
                self.ipcev_is_set.wait();
                var source: *VMNode = getNode(self.absolute_source_id);
                source.ipcev_done.wait();
                self.value = source.value;
            },
            .phi_setter => {
                var destination: *VMNode = getNode(self.phi_setter_absolute_destination_id);
                destination.absolute_source_id = self.phi_setter_absolute_source_id;
                destination.ipcev_is_set.signal();
            },
            .scope_instantiator => {
                SHARED_GLOBALS.instancing_mutex.lock();
                var instancing_done: *IPC_Event = try SHARED_GLOBALS.allocator.create(IPC_Event);
                if (self.scope_template_index >= SHARED_GLOBALS.scope_templates.len) unreachable;
                var scope_template: ScopeTemplate = SHARED_GLOBALS.scope_templates[self.scope_template_index];
                var new_instance_id_base = SHARED_GLOBALS.next_instance_base;
                if (new_instance_id_base + scope_template.node_templates.len >= SharedGlobals.MAX_NUM_VMNODES) unreachable;
                var args_size = self.scope_args.len;
                if (args_size != scope_template.num_params) unreachable;
                for (0..args_size) |i| {
                    var instance: *VMNode = getNode(new_instance_id_base + i);
                    var template: *VMNode = &scope_template.node_templates[i];
                    instance.* = template.*;
                    if (instance.id != i) unreachable;
                    instance.ipcev_instancing_done = instancing_done;
                    instance.instance_id_base = new_instance_id_base;

                    if (instance.node_type != .phi) unreachable;
                    instance.absolute_source_id = self.instance_id_base + self.scope_args[i];
                    instance.ipcev_is_set.signal();
                    var pid = try std.os.fork();
                    if (pid == 0) {
                        setPdeathsig();
                        try instance.process();
                        std.os.exit(0);
                    }
                }
                for (args_size..scope_template.node_templates.len) |i| {
                    var instance: *VMNode = getNode(new_instance_id_base + i);
                    var template: *VMNode = &scope_template.node_templates[i];
                    instance.* = template.*;
                    if (instance.id != i) unreachable;
                    instance.ipcev_instancing_done = instancing_done;
                    instance.instance_id_base = new_instance_id_base;

                    switch (instance.node_type) {
                        .phi_setter => {
                            instance.phi_setter_absolute_source_id = instance.instance_id_base + instance.phi_setter_source_id;
                            if (instance.phi_setter_destination_up == 0) {
                                instance.phi_setter_absolute_destination_id = instance.instance_id_base + instance.phi_setter_destination_id;
                            } else {
                                var loop_root: *VMNode = getNode(self.scope_loop_root);
                                instance.phi_setter_absolute_destination_id = loop_root.instance_id_base + instance.phi_setter_destination_id;
                            }
                        },
                        .scope_instantiator => {
                            instance.scope_iteration = 0;
                            if (instance.scope_template_index == self.scope_template_index) {
                                instance.scope_iteration = self.scope_iteration + 1;
                            }
                            if (instance.scope_iteration == 0) {
                                instance.scope_loop_root = instance.instance_id_base + instance.id;
                            } else {
                                instance.scope_loop_root = self.scope_loop_root;
                            }
                        },
                        else => {},
                    }
                    var pid = try std.os.fork();
                    if (pid == 0) {
                        setPdeathsig();
                        try instance.process();
                        std.os.exit(0);
                    }
                }
                SHARED_GLOBALS.next_instance_base += scope_template.node_templates.len;
                SHARED_GLOBALS.instancing_mutex.unlock();
                instancing_done.signal();
                if (scope_template.ret_id) |ret_id| {
                    var ret_instance: *VMNode = getNode(new_instance_id_base + ret_id);
                    ret_instance.ipcev_done.wait();
                    self.value = ret_instance.value;
                }
                self.ipcev_done.signal();
                waitAllChildren();
                return;
            },
        }
        self.ipcev_done.signal();
    }
};

const ScopeTemplate = struct {
    num_params: u32,
    ret_id: ?u32,
    node_templates: []VMNode,
};


pub fn loadNodeTemplate(reader: anytype) !VMNode {
    var id = try reader.readIntNative(u32);
    var num_requirements = try reader.readIntNative(u32);
    var requirements = try SHARED_GLOBALS.allocator.alloc(u32, num_requirements);
    for (0..num_requirements) |i| {
        requirements[i] = try reader.readIntNative(u32);
    }
    var node_type_int = try reader.readIntNative(u32);
    var node_type = @as(VMNodeType, @enumFromInt(node_type_int));
    var vmnode = VMNode {
        .node_type = node_type,
        .id = id,
        .requirements = requirements,
    };
    switch (node_type) {
        .constant => vmnode.constant_value = Value {.int = try reader.readIntNative(i64)},
        .compute => {
            var op_type_int = try reader.readIntNative(u32);
            var op_type = @as(ComputeOpType, @enumFromInt(op_type_int));
            vmnode.op = op_type;
            var operand_id_1 = try reader.readIntNative(i32);
            var operand_id_2 = try reader.readIntNative(i32);
            var operand_id_3 = try reader.readIntNative(i32);
            vmnode.operand_id_1 = if (operand_id_1 >= 0) @as(u32, @bitCast(operand_id_1)) else null;
            vmnode.operand_id_2 = if (operand_id_2 >= 0) @as(u32, @bitCast(operand_id_2)) else null;
            vmnode.operand_id_3 = if (operand_id_3 >= 0) @as(u32, @bitCast(operand_id_3)) else null;
        },
        .vector => {
            var vector_size = try reader.readIntNative(u32);
            vmnode.vector_element_ids = try SHARED_GLOBALS.allocator.alloc(u32, vector_size);
            for (0..vector_size) |i| {
                vmnode.vector_element_ids[i] = try reader.readIntNative(u32);
            }
        },
        .scope_instantiator => {
            vmnode.scope_template_index = try reader.readIntNative(u32);
            var scope_args_size = try reader.readIntNative(u32);
            vmnode.scope_args = try SHARED_GLOBALS.allocator.alloc(u32, scope_args_size);
            for (0..scope_args_size) |i| {
                vmnode.scope_args[i] = try reader.readIntNative(u32);
            }
        },
        .phi => {},
        .phi_setter => {
            vmnode.phi_setter_source_id = try reader.readIntNative(u32);
            vmnode.phi_setter_destination_id = try reader.readIntNative(u32);
            vmnode.phi_setter_destination_up = try reader.readIntNative(u32);
        }
    }
    return vmnode;
}
pub fn loadScopeTemplate(reader: anytype) !ScopeTemplate {
    var num_params = try reader.readIntNative(u32);
    var ret_id = try reader.readIntNative(i32);
    var num_node_templates = try reader.readIntNative(u32);
    var node_templates = try SHARED_GLOBALS.allocator.alloc(VMNode, num_node_templates);
    for (0..num_node_templates) |i| {
        node_templates[i] = try loadNodeTemplate(reader);
    }
    return ScopeTemplate {.num_params = num_params, .ret_id = if (ret_id >= 0) @as(u32, @bitCast(ret_id)) else null, .node_templates = node_templates};
}
pub fn loadProgram(path: []const u8) !void {
    var buf = try std.fs.cwd().readFileAlloc(SHARED_GLOBALS.allocator, path, 1 << 20);
    var stream = std.io.fixedBufferStream(buf);
    var reader = stream.reader();
    var num_scope_templates = try reader.readIntNative(u32);
    SHARED_GLOBALS.scope_templates = try SHARED_GLOBALS.allocator.alloc(ScopeTemplate, num_scope_templates);
    for (0..num_scope_templates) |i| {
        SHARED_GLOBALS.scope_templates[i] = try loadScopeTemplate(reader);
    }
    _ = reader.readByte() catch {
        return;
    };
    unreachable;
}


pub fn main() !void {
    var fn_main_gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const fn_main_gpaa = fn_main_gpa.allocator();

    SHARED_GLOBALS = try fn_main_gpaa.create(SharedGlobals);
    SHARED_GLOBALS.fba = std.heap.FixedBufferAllocator.init(&SHARED_GLOBALS.fba_buf);
    SHARED_GLOBALS.allocator = SHARED_GLOBALS.fba.threadSafeAllocator();

    SHARED_GLOBALS.instancing_mutex = std.Thread.Mutex{};
    var dummy_req = try SHARED_GLOBALS.allocator.alloc(u32, 0);
    for (0..SharedGlobals.MAX_NUM_VMNODES) |i| {
        SHARED_GLOBALS.nodes[i] = VMNode {.node_type = .constant, .id = 0, .requirements = dummy_req};
    }

    const args = try std.process.argsAlloc(SHARED_GLOBALS.allocator);
    defer std.process.argsFree(SHARED_GLOBALS.allocator, args);

    if (args.len != 2) {
        std.debug.print("Usage: ./forkmachine <path/to/program>\n", .{});
        std.os.exit(1);
    }

    try loadProgram(args[1]);
    std.debug.print("Program loaded.\n", .{});

    var big_bang: *IPC_Event = try SHARED_GLOBALS.allocator.create(IPC_Event);
    var init_node: *VMNode = getNode(0);
    init_node.node_type = .scope_instantiator;
    init_node.instance_id_base = 0;
    init_node.id = 0;
    init_node.ipcev_instancing_done = big_bang;
    init_node.requirements = try SHARED_GLOBALS.allocator.alloc(u32, 0);
    init_node.scope_template_index = 0;
    init_node.scope_iteration = 0;
    init_node.scope_loop_root = 0;
    SHARED_GLOBALS.next_instance_base = 1;

    var num_init_scope_args = SHARED_GLOBALS.scope_templates[0].num_params;
    switch (num_init_scope_args) {
        0 => {
            std.debug.print("The program does not ask for input.\n", .{});
            init_node.scope_args = try SHARED_GLOBALS.allocator.alloc(u32, 0);
        },
        1 => {
            std.debug.print("The program asks for input.\n", .{});

            var arg_node: *VMNode = getNode(1);
            arg_node.node_type = .constant;
            arg_node.instance_id_base = 0;
            arg_node.id = 1;
            const stdin = std.io.getStdIn();
            var input = try stdin.reader().readUntilDelimiterAlloc(SHARED_GLOBALS.allocator, '\n', 256);
            defer SHARED_GLOBALS.allocator.free(input);
            var values = try SHARED_GLOBALS.allocator.alloc(Value, input.len);
            for (0..values.len) |i| {
                values[i] = Value {.int = input[i]};
            }
            arg_node.value = Value {.vector = values};
            arg_node.ipcev_done.signal();
            SHARED_GLOBALS.next_instance_base += 1;

            init_node.scope_args = try SHARED_GLOBALS.allocator.alloc(u32, 1);
            init_node.scope_args[0] = 1;
        },
        else => unreachable,
    }

    std.debug.print("Starting execution.\n===================\n", .{});
    var pid = try std.os.fork();
    if (pid == 0) {
        setPdeathsig();
        try init_node.process();
        std.os.exit(0);
    } else {
        big_bang.signal();
        init_node.ipcev_done.wait();
        std.debug.print("Return value: ", .{});
        init_node.value.print();
        std.debug.print("\n", .{});
        std.debug.print("String interpretation: \"", .{});
        init_node.value.print_string();
        std.debug.print("\"\n", .{});
    }
    std.debug.print("===================\nEnd of program.\n", .{});
    std.debug.print("{} nodes instanced. (sizeof(node) == {})\n", .{SHARED_GLOBALS.next_instance_base, @sizeOf(VMNode)});
    std.debug.print("{} bytes allocated for values etc.\n", .{SHARED_GLOBALS.fba.end_index});
}
