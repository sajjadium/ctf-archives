use core::arch::asm;

use crate::util::*;
use crate::prelude::*;
use crate::sync::IMutex;

const GDT_SIZE: usize = 5;

#[repr(C, packed)]
#[derive(Debug)]
pub struct Gdt {
	entries: [GdtEntry; GDT_SIZE],
	tss: TssEntry,
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
struct GdtPointer {
	limit: u16,
	base: u64,
}

impl Gdt {
	pub const fn new() -> Self {
		Gdt {
			entries: [
				GdtEntry::null(),
				GdtEntry::kernel_code(),
				GdtEntry::kernel_data(),
				GdtEntry::user_data(),
				GdtEntry::user_code(),
			],
			tss: TssEntry::new(),
		}
	}

	fn load(&mut self, tss: &Tss) {
        self.tss.set_tss_addr(tss);

		let gdtptr = GdtPointer {
			limit: (size_of::<Gdt>() - 1) as _,
			base: (self as *const _) as _,
		};

		unsafe {
			asm!("lgdt [{}]", in(reg) &gdtptr, options(nostack));
		}
	}
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
struct GdtEntry {
	limit1: u16,
	base1: u16,
	base2: u8,
	access: u8,
	limit2_flags: u8,
	base3: u8,
}

impl GdtEntry {
	const fn new(base: u32, limit: u32, access: u8, flags: u8) -> Self {
		let base = base as usize;
		let limit = limit as usize;
		GdtEntry {
			base1: get_bits(base, 0..16) as _,
			base2: get_bits(base, 16..24) as _,
			base3: get_bits(base, 24..32) as _,
			access,
			limit1: get_bits(limit, 0..16) as _,
			limit2_flags: get_bits(limit, 16..20) as u8 | ((flags & 0xf) << 4),
		}
	}

	const fn null() -> Self {
		Self::new(0, 0, 0, 0)
	}

	const fn kernel_code() -> Self {
		Self::new(0, 0xffffffff, 0x9a, 0x0a)
	}

	const fn kernel_data() -> Self {
		Self::new(0, 0xffffffff, 0x92, 0x0a)
	}

	const fn user_code() -> Self {
		Self::new(0, 0xffffffff, 0xfa, 0x0a)
	}

	const fn user_data() -> Self {
		Self::new(0, 0xffffffff, 0xf2, 0x0a)
	}
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct Tss {
	zero1: u32,
	pub rsp0: u64,
	rsp1: u64,
	rsp2: u64,
	zero2: u64,
	ist1: u64,
	ist2: u64,
	ist3: u64,
	ist4: u64,
	ist5: u64,
	ist6: u64,
	ist7: u64,
	zero3: u64,
	zero4: u16,
	iomap: u16,
}

impl Tss {
	pub const fn new() -> Self {
		Tss {
			rsp0: 0,
			rsp1: 0,
			rsp2: 0,
			ist1: 0,
			ist2: 0,
			ist3: 0,
			ist4: 0,
			ist5: 0,
			ist6: 0,
			ist7: 0,
			zero1: 0,
			zero2: 0,
			zero3: 0,
			zero4: 0,
			iomap: size_of::<Tss>() as u16,
		}
	}
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
struct TssEntry {
	limit1: u16,
	base1: u16,
	base2: u8,
	access: u8,
	limit2_flags: u8,
	base3: u8,
	base4: u32,
	zero: u32,
}

impl TssEntry {
	const fn new() -> Self {
		TssEntry {
			base1: 0,
			base2: 0,
			base3: 0,
			base4: 0,
			access: 0x89,
			limit1: (size_of::<Tss>() - 1) as _,
			limit2_flags: 0,
			zero: 0,
		}
	}

    fn set_tss_addr(&mut self, tss: &Tss) {
        let addr = (tss as *const _) as usize;
        self.base1 = get_bits(addr, 0..16) as _;
		self.base2 = get_bits(addr, 16..24) as _;
		self.base3 = get_bits(addr, 24..32) as _;
		self.base4 = get_bits(addr, 32..64) as _;
    }
}

pub static GDT: IMutex<Gdt> = IMutex::new(Gdt::new());
pub static TSS: IMutex<Tss> = IMutex::new(Tss::new());

pub fn init() {
	GDT.lock().load(&TSS.lock());

	unsafe {
		asm!("ltr di",
			inout("di") 0x28 => _,
		);
	}
}
