pub inline fn in8(port: usize) u8 {
    return asm volatile (
        \\.intel_syntax noprefix
        \\in al, dx
        \\.att_syntax prefix
        : [ret] "={rax}" (-> u8),
        : [port] "{rdx}" (port),
    );
}

pub const inb = in8;

pub inline fn out8(port: usize, b: u8) void {
    asm volatile (
        \\.intel_syntax noprefix
        \\out dx, al
        \\.att_syntax prefix
        :
        : [port] "{rdx}" (port),
          [b] "{rax}" (b),
    );
}

pub const outb = out8;

pub inline fn in16(port: usize) u16 {
    return asm volatile (
        \\.intel_syntax noprefix
        \\in ax, dx
        \\.att_syntax prefix
        : [ret] "={rax}" (-> u16),
        : [port] "{rdx}" (port),
    );
}

pub inline fn out16(port: usize, w: u16) void {
    asm volatile (
        \\.intel_syntax noprefix
        \\out dx, ax
        \\.att_syntax prefix
        :
        : [port] "{rdx}" (port),
          [w] "{rax}" (w),
    );
}

pub inline fn in32(port: usize) u32 {
    return asm volatile (
        \\.intel_syntax noprefix
        \\in eax, dx
        \\.att_syntax prefix
        : [ret] "={rax}" (-> u32),
        : [port] "{rdx}" (port),
    );
}

pub inline fn out32(port: usize, d: u32) void {
    asm volatile (
        \\.intel_syntax noprefix
        \\out dx, eax
        \\.att_syntax prefix
        :
        : [port] "{rdx}" (port),
          [d] "{rax}" (d),
    );
}

pub inline fn in64(port: usize) u64 {
    return asm volatile (
        \\.intel_syntax noprefix
        \\in rax, dx
        \\.att_syntax prefix
        : [ret] "={rax}" (-> u64),
        : [port] "{rdx}" (port),
    );
}

pub inline fn out64(port: usize, q: u64) void {
    asm volatile (
        \\.intel_syntax noprefix
        \\out dx, rax
        \\.att_syntax prefix
        :
        : [port] "{rdx}" (port),
          [q] "{rax}" (q),
    );
}

pub inline fn wait() void {
    out8(0x80, 0);
}
