use spin::Lazy;

use crate::prelude::*;
use crate::sched;
use crate::arch::x64::get_cr2;
use idt::Idt;

use pic::{PICM_OFFSET, PICS_OFFSET};

pub mod idt;
mod pic;
pub mod pit;

pub const EXC_DIVIDE_BY_ZERO: u8 = 0;
pub const EXC_DEBUG: u8 = 1;
pub const EXC_NON_MASK_INTERRUPT: u8 = 2;
pub const EXC_BREAKPOINT: u8 = 3;
pub const EXC_OVERFLOW: u8 = 4;
pub const EXC_BOUND_RANGE_EXCEED: u8 = 5;
pub const EXC_INVALID_OPCODE: u8 = 6;
pub const EXC_DEVICE_UNAVAILABLE: u8 = 7;
pub const EXC_DOUBLE_FAULT: u8 = 8;
pub const EXC_NONE_9: u8 = 9;
pub const EXC_INVALID_TSS: u8 = 10;
pub const EXC_SEGMENT_NOT_PRESENT: u8 = 11;
pub const EXC_STACK_SEGMENT_FULL: u8 = 12;
pub const EXC_GENERAL_PROTECTION_FAULT: u8 = 13;
pub const EXC_PAGE_FAULT: u8 = 14;

pub const PAGE_FAULT_PROTECTION: u64 = 1;
pub const PAGE_FAULT_WRITE: u64 = 1 << 1;
pub const PAGE_FAULT_USER: u64 = 1 << 2;
pub const PAGE_FAULT_RESERVED: u64 = 1 << 3;
pub const PAGE_FAULT_EXECUTE: u64 = 1 << 4;

pub const EXC_NONE_15: u8 = 15;
pub const EXC_X87_FLOATING_POINT: u8 = 16;
pub const EXC_ALIGNMENT_CHECK: u8 = 17;
pub const EXC_MACHINE_CHECK: u8 = 18;
pub const EXC_SIMD_FLOATING_POINT: u8 = 19;
pub const EXC_VIRTUALIZATION: u8 = 20;
pub const EXC_NONE_21: u8 = 21;
pub const EXC_NONE_22: u8 = 22;
pub const EXC_NONE_23: u8 = 23;
pub const EXC_NONE_24: u8 = 24;
pub const EXC_NONE_25: u8 = 25;
pub const EXC_NONE_26: u8 = 26;
pub const EXC_NONE_27: u8 = 27;
pub const EXC_NONE_28: u8 = 28;
pub const EXC_NONE_29: u8 = 29;
pub const EXC_SECURITY: u8 = 30;
pub const EXC_NONE_31: u8 = 31;

pub const IRQ_BASE: u8 = 32;

pub const IRQ_PIT_TIMER: u8 = IRQ_BASE;
pub const IRQ_KEYBOARD: u8 = IRQ_BASE + 1;
pub const IRQ_SERIAL_PORT_2: u8 = IRQ_BASE + 3;
pub const IRQ_SERIAL_PORT_1: u8 = IRQ_BASE + 4;
pub const IRQ_PARALLEL_PORT_2_3: u8 = IRQ_BASE + 5;
pub const IRQ_FLOPPY_DISK: u8 = IRQ_BASE + 6;
pub const IRQ_PARALLEL_PORT_1: u8 = IRQ_BASE + 7;

pub const IRQ_CLOCK: u8 = IRQ_BASE + 8;
pub const IRQ_ACPI: u8 = IRQ_BASE + 9;
pub const IRQ_NONE_1: u8 = IRQ_BASE + 10;
pub const IRQ_NONE_2: u8 = IRQ_BASE + 11;
pub const IRQ_MOUSE: u8 = IRQ_BASE + 12;
pub const IRQ_CO_PROCESSOR: u8 = IRQ_BASE + 13;
pub const IRQ_PRIMARY_ATA: u8 = IRQ_BASE + 14;
pub const IRQ_SECONDARY_ATA: u8 = IRQ_BASE + 15;

pub const SPURIOUS: u8 = 0xf0;


#[derive(Debug, Clone, Copy)]
#[repr(C)]
pub struct Registers {
    pub rax: usize,
    pub rbx: usize,
    pub rcx: usize,
    pub rdx: usize,
    pub rbp: usize,
    pub rsp: usize,
    pub rdi: usize,
    pub rsi: usize,
    pub r8: usize,
    pub r9: usize,
    pub r10: usize,
    pub r11: usize,
    pub r12: usize,
    pub r13: usize,
    pub r14: usize,
    pub r15: usize,
    pub rflags: usize,
    pub rip: usize,
    pub cs: u16,
    pub ss: u16,
}

fn double_fault(registers: &Registers) {
    panic!("double fault\nregisters:\n{:x?}", registers);
}

fn gp_exception(registers: &Registers) {
    println!("general protection exception\nregisters:\n{:x?}", registers);
}

fn page_fault(registers: &Registers, error_code: u64) {
    println!("error code: {:x}", error_code);
    let ring = if error_code & PAGE_FAULT_USER != 0 {
		"user"
	} else {
		"kernel"
	};

	let action = if error_code & PAGE_FAULT_EXECUTE != 0 {
		"instruction fetch"
	} else if error_code & PAGE_FAULT_WRITE != 0 {
		"write"
	} else {
		"read"
	};

	println!(
		r"page fault accessing virtual address {:x}
page fault during {} {}
non present page: {}
reserved bit set: {}
registers:
{:x?}",
		get_cr2(),
		ring,
		action,
		error_code & PAGE_FAULT_PROTECTION == 0,
		error_code & PAGE_FAULT_RESERVED != 0,
		registers
	);
}

#[no_mangle]
extern "C" fn rust_int_handler(int_num: u8, registers: &Registers, error_code: u64) {
    match int_num {
        EXC_DOUBLE_FAULT => double_fault(registers),
        EXC_GENERAL_PROTECTION_FAULT => gp_exception(registers),
        EXC_PAGE_FAULT => page_fault(registers, error_code),
        IRQ_PIT_TIMER => {
            pit().irq_handler();
            sched::timer_handler();
        },
        _ => (),
    }
}

#[no_mangle]
pub extern "C" fn eoi() {
    pic::eoi(false)
}

pub static IDT: Lazy<Idt> = Lazy::new(|| Idt::new());

pub fn pit() -> &'static pit::Pit {
    pit::PIT.get().expect("pit not initialized")
}

pub fn init() {
    pic::remap(PICM_OFFSET, PICS_OFFSET);
    pit::PIT.call_once(|| pit::Pit::new(0xffff));
    IDT.load();
}