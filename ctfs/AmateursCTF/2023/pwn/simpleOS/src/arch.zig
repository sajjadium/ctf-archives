pub const Gdtr64 = packed struct {
    size: u16,
    offset: u64,
};

pub fn read_gdtr64() Gdtr64 {
    var gdtr: Gdtr64 = undefined;
    asm volatile (
        \\.intel_syntax noprefix
        \\sgdt qword ptr [rax]
        \\.att_syntax prefix
        :
        : [gdtr] "{rax}" (&gdtr),
    );
    return gdtr;
}

pub const Idtr64 = packed struct {
    size: u16,
    offset: u64,
};

pub fn read_idtr64() Idtr64 {
    var idtr: Idtr64 = undefined;
    asm volatile (
        \\.intel_syntax noprefix
        \\sidt qword ptr [rax]
        \\.att_syntax prefix
        :
        : [idtr] "{rax}" (&idtr),
    );
    return idtr;
}

pub fn read_cr2() u64 {
    var cr2: u64 = undefined;
    asm volatile (
        \\.intel_syntax noprefix
        \\mov rax, cr2
        \\.att_syntax prefix
        : [cr2] "={rax}" (cr2),
    );
    return cr2;
}

pub const Cr3 = packed struct {
    flags: u12,
    pml4: u52,
};

pub fn read_cr3() Cr3 {
    var cr3: u64 = undefined;
    asm volatile (
        \\.intel_syntax noprefix
        \\mov rax, cr3
        \\.att_syntax prefix
        : [cr3] "={rax}" (cr3),
    );
    return @bitCast(Cr3, cr3);
}

pub fn read_sp() usize {
    var sp: usize = undefined;
    asm volatile (
        \\.intel_syntax noprefix
        \\mov rax, rsp
        \\.att_syntax prefix
        : [sp] "={sp}" (sp),
    );
    return sp;
}

pub fn hang() noreturn {
    asm volatile ("hlt");
    while (true) {}
}

pub fn pause() void {
    asm volatile ("pause");
}
