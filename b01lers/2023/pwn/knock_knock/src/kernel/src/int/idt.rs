use core::arch::asm;

use crate::prelude::*;

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
struct IdtEntry {
    addr1: u16,
    code_selector: u16,
    ist: u8,
    attr: u8,
    addr2: u16,
    addr3: u32,
    zero: u32,
}

impl IdtEntry {
    fn new(addr: usize) -> Self {
        IdtEntry {
            addr1: get_bits(addr, 0..16) as _,
            addr2: get_bits(addr, 16..32) as _,
            addr3: get_bits(addr, 32..64) as _,
            code_selector: 8,
            ist: 0,
            attr: 0xee,
            zero: 0,
        }
    }

    fn none() -> Self {
        IdtEntry {
            addr1: 0,
            addr2: 0,
            addr3: 0,
            code_selector: 0,
            ist: 0,
            attr: 0,
            zero: 0,
        }
    }
}

macro_rules! make_idt_entry {
    ($idt:expr, $num:literal) => {
        concat_idents::concat_idents!(fn_name = int_handler_, $num {
            extern "C" {
                fn fn_name();
            }
            $idt.entries[$num] = IdtEntry::new(fn_name as usize);
        })
    };
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
struct IdtPointer {
    limit: u16,
    base: u64,
}

#[derive(Debug)]
pub struct Idt {
    entries: [IdtEntry; Self::NUM_ENTRIES],
}

impl Idt {
    const NUM_ENTRIES: usize = 256;

    pub fn new() -> Self {
        let mut out = Idt {
            entries: [IdtEntry::none(); Self::NUM_ENTRIES],
        };

        make_idt_entry!(out, 0);
        make_idt_entry!(out, 1);
        make_idt_entry!(out, 2);
        make_idt_entry!(out, 3);
        make_idt_entry!(out, 4);
        make_idt_entry!(out, 5);
        make_idt_entry!(out, 6);
        make_idt_entry!(out, 7);
        make_idt_entry!(out, 8);
        make_idt_entry!(out, 9);
        make_idt_entry!(out, 10);
        make_idt_entry!(out, 11);
        make_idt_entry!(out, 12);
        make_idt_entry!(out, 13);
        make_idt_entry!(out, 14);
        make_idt_entry!(out, 15);
        make_idt_entry!(out, 16);
        make_idt_entry!(out, 17);
        make_idt_entry!(out, 18);
        make_idt_entry!(out, 19);
        make_idt_entry!(out, 20);
        make_idt_entry!(out, 21);
        make_idt_entry!(out, 22);
        make_idt_entry!(out, 23);
        make_idt_entry!(out, 24);
        make_idt_entry!(out, 25);
        make_idt_entry!(out, 26);
        make_idt_entry!(out, 27);
        make_idt_entry!(out, 28);
        make_idt_entry!(out, 29);
        make_idt_entry!(out, 30);
        make_idt_entry!(out, 31);

        make_idt_entry!(out, 32);
        make_idt_entry!(out, 33);
        make_idt_entry!(out, 34);
        make_idt_entry!(out, 35);
        make_idt_entry!(out, 36);
        make_idt_entry!(out, 37);
        make_idt_entry!(out, 38);
        make_idt_entry!(out, 39);
        make_idt_entry!(out, 40);
        make_idt_entry!(out, 41);
        make_idt_entry!(out, 42);
        make_idt_entry!(out, 43);
        make_idt_entry!(out, 44);
        make_idt_entry!(out, 45);
        make_idt_entry!(out, 46);
        make_idt_entry!(out, 47);

        out
    }

    pub fn load(&self) {
        let idt_pointer = IdtPointer {
            limit: (size_of::<[IdtEntry; Self::NUM_ENTRIES]>() - 1) as _,
            base: &self.entries as *const _ as _,
        };

        unsafe {
            asm!("lidt [{}]", in(reg) &idt_pointer, options(nostack));
        }
    }
}
