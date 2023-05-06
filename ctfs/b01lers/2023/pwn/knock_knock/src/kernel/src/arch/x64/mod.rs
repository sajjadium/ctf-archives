use core::arch::asm;
use core::time::Duration;

use crate::prelude::*;

pub const EFER_MSR: u32 = 0xc0000080;
pub const EFER_EXEC_DISABLE: u64 = 1 << 11;
pub const EFER_SYSCALL_ENABLE: u64 = 1;

pub const FSBASE_MSR: u32 = 0xc0000100;
pub const GSBASE_MSR: u32 = 0xc0000101;
pub const GSBASEK_MSR: u32 = 0xc0000102;

pub const STAR_MSR: u32 = 0xc0000081;
pub const LSTAR_MSR: u32 = 0xc0000082;
pub const RTAR_MSR: u32 = 0xc0000083;
pub const FMASK_MSR: u32 = 0xc0000084;

#[inline]
pub fn rdmsr(msr: u32) -> u64 {
    let low: u32;
    let high: u32;
    unsafe {
        asm!("rdmsr", in("ecx") msr, out("eax") low, out("edx") high, options(nomem, nostack));
    }
    ((high as u64) << 32) | low as u64
}

#[inline]
pub fn wrmsr(msr: u32, data: u64) {
    let low = get_bits(data as usize, 0..32);
    let high = get_bits(data as usize, 32..64);
    unsafe {
        asm!("wrmsr", in("ecx") msr, in("eax") low, in("edx") high, options(nomem, nostack));
    }
}

#[inline]
pub fn hlt() {
    unsafe {
        asm!("hlt", options(nomem, nostack));
    }
}

pub const RFLAGS_INT: usize = 1 << 9;

#[inline]
pub fn get_flags() -> usize {
    let out;
    unsafe {
        asm!("pushfq\npop {}", out(reg) out, options(nomem));
    }
    out
}

#[inline]
pub fn set_flags(flags: usize) {
    unsafe {
        asm!("push {}\npopfq", in(reg) flags);
    }
}

#[inline]
pub fn cli() {
    unsafe {
        asm!("cli", options(nomem, nostack));
    }
}

#[inline]
pub fn sti() {
    unsafe {
        asm!("sti", options(nomem, nostack));
    }
}

#[inline]
pub fn sti_nop() {
    unsafe {
        asm!("sti\nnop", options(nomem, nostack));
    }
}

#[inline]
pub fn sti_hlt() {
    unsafe {
        asm!("sti\nhlt", options(nomem, nostack));
    }
}

pub fn is_int_enabled() -> bool {
    get_flags() & RFLAGS_INT != 0
}

pub fn set_int_enabled(enabled: bool) {
    if enabled {
        sti_nop();
    } else {
        cli();
    }
}

#[derive(Debug)]
pub struct IntDisable {
    old_status: bool,
}

impl IntDisable {
    pub fn new() -> Self {
        let old_status = is_int_enabled();
        cli();
        IntDisable {
            old_status,
        }
    }

    pub fn old_is_enabled(&self) -> bool {
        self.old_status
    }
}

impl Drop for IntDisable {
    fn drop(&mut self) {
        set_int_enabled(self.old_status);
    }
}

#[inline]
pub fn outb(port: u16, data: u8) {
    unsafe {
        asm!("out dx, al", in("dx") port, in("al") data);
    }
}

#[inline]
pub fn outw(port: u16, data: u16) {
    unsafe {
        asm!("out dx, al", in("dx") port, in("ax") data);
    }
}

#[inline]
pub fn outd(port: u16, data: u32) {
    unsafe {
        asm!("out dx, al", in("dx") port, in("eax") data);
    }
}

#[inline]
pub fn inb(port: u16) -> u8 {
    let out;
    unsafe {
        asm!("in al, dx", in("dx") port, out("al") out);
    }
    out
}

#[inline]
pub fn inw(port: u16) -> u16 {
    let out;
    unsafe {
        asm!("in ax, dx", in("dx") port, out("ax") out);
    }
    out
}

#[inline]
pub fn ind(port: u16) -> u32 {
    let out;
    unsafe {
        asm!("in eax, dx", in("dx") port, out("eax") out);
    }
    out
}

#[inline]
pub fn io_wait(time: Duration) {
    for _ in 0..time.as_micros() {
        inb(0x80);
    }
}

#[inline]
pub fn get_cr0() -> usize {
    let out;
    unsafe {
        asm!("mov {}, cr0", out(reg) out, options(nomem, nostack));
    }
    out
}

#[inline]
pub fn set_cr0(n: usize) {
    unsafe {
        asm!("mov cr0, {}", in(reg) n, options(nomem, nostack));
    }
}

#[inline]
pub fn get_cr2() -> usize {
    let out;
    unsafe {
        asm!("mov {}, cr2", out(reg) out, options(nomem, nostack));
    }
    out
}

#[inline]
pub fn set_cr2(n: usize) {
    unsafe {
        asm!("mov cr2, {}", in(reg) n, options(nomem, nostack));
    }
}

#[inline]
pub fn get_cr3() -> usize {
    let out;
    unsafe {
        asm!("mov {}, cr3", out(reg) out, options(nomem, nostack));
    }
    out
}

#[inline]
pub fn set_cr3(n: usize) {
    unsafe {
        asm!("mov cr3, {}", in(reg) n, options(nomem, nostack));
    }
}

#[inline]
pub fn get_cr4() -> usize {
    let out;
    unsafe {
        asm!("mov {}, cr4", out(reg) out, options(nomem, nostack));
    }
    out
}

#[inline]
pub fn set_cr4(n: usize) {
    unsafe {
        asm!("mov cr4, {}", in(reg) n, options(nomem, nostack));
    }
}

#[inline]
pub fn get_rsp() -> usize {
    let out;
    unsafe {
        asm!("mov {}, rsp", out(reg) out, options(nomem));
    }
    out
}

#[inline]
pub fn invlpg(addr: usize) {
    unsafe {
        asm!("invlpg [{}]", in (reg) addr);
    }
}

extern "C" {
    fn asm_gs_addr() -> usize;
    pub fn asm_switch_thread(new_rsp: usize);
    pub fn asm_thread_init();
}

pub fn gs_addr() -> usize {
    unsafe { asm_gs_addr() }
}