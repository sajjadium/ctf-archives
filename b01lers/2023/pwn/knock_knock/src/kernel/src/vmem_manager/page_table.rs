use bitflags::bitflags;

use crate::prelude::*;
use crate::allocation::zm;
use crate::mem::Allocation;
use super::PageMappingFlags;

const PAGE_ADDR_BITMASK: usize = 0x000ffffffffff000;

bitflags! {
	pub struct PageTableFlags: usize {
		const NONE = 		0;
		const PRESENT = 	1;
		const WRITABLE = 	1 << 1;
		const USER = 		1 << 2;
		const PWT = 		1 << 3;
		const PCD = 		1 << 4;
		const ACCESSED = 	1 << 5;
		const DIRTY = 		1 << 6;
		const HUGE = 		1 << 7;
		const GLOBAL = 		1 << 8;
		const NO_EXEC =		1 << 63;
	}
}

impl PageTableFlags {
	fn present(&self) -> bool {
		self.contains(Self::PRESENT)
	}
}

impl From<PageMappingFlags> for PageTableFlags {
    fn from(flags: PageMappingFlags) -> Self {
		let mut out = PageTableFlags::NONE;
		if flags.contains(PageMappingFlags::WRITE) {
			out |= PageTableFlags::WRITABLE;
		}

		if !flags.contains(PageMappingFlags::EXEC) {
			out |= PageTableFlags::NO_EXEC;
		}

		if flags.exists() {
			out |= PageTableFlags::PRESENT;
		}

		if flags.contains(PageMappingFlags::USER) {
			out |= PageTableFlags::USER;
		}

		out
    }
}

#[repr(transparent)]
#[derive(Debug, Clone, Copy)]
pub struct PageTablePointer(usize);

impl PageTablePointer {
	pub fn new(addr: PhysAddr, flags: PageTableFlags) -> Self {
		let addr = addr.as_usize();
		PageTablePointer(addr | flags.bits())
	}

	pub fn as_mut_ptr(&mut self) -> *mut PageTable {
		if self.0 & PageTableFlags::PRESENT.bits() == 0 {
			null_mut()
		} else {
			phys_to_virt(self.0 & PAGE_ADDR_BITMASK) as *mut PageTable
		}
	}

	fn flags(&self) -> PageTableFlags {
		PageTableFlags::from_bits_truncate(self.0)
	}

	unsafe fn set_flags(&mut self, flags: PageTableFlags) {
		self.0 = (self.0 & PAGE_ADDR_BITMASK) | flags.bits();
	}

    pub fn address(&self) -> PhysAddr {
        PhysAddr::new(self.0 & PAGE_ADDR_BITMASK)
    }
}

#[repr(transparent)]
#[derive(Debug)]
pub struct PageTable([PageTablePointer; PAGE_SIZE / 8]);

impl PageTable {
	pub fn new(
		flags: PageTableFlags,
	) -> Option<PageTablePointer> {
		let frame = zm().alloc(PAGE_SIZE)?.as_usize();

		unsafe {
			memset(frame as *mut u8, PAGE_SIZE, 0);
		}

		let addr = virt_to_phys(frame);
		let flags = flags | PageTableFlags::PRESENT;

		Some(PageTablePointer(addr | flags.bits()))
	}

	pub fn entry_count(&self) -> usize {
		get_bits(self.0[0].0, 52..63)
	}

	fn set_entry_count(&mut self, n: usize) {
		let n = get_bits(n, 0..11);
		let ptr_no_count = self.0[0].0 & 0x800fffffffffffff;
		self.0[0] = PageTablePointer(ptr_no_count | (n << 52));
	}

	fn inc_entry_count(&mut self, n: isize) {
		self.set_entry_count((self.entry_count() as isize + n) as _);
	}

	fn present(&self, index: usize) -> bool {
		(self.0[index].0 & PageTableFlags::PRESENT.bits()) != 0
	}

	pub unsafe fn dealloc(&mut self) {
		let frame = Allocation::new(self.addr(), PAGE_SIZE);
        unsafe { zm().dealloc(frame); }
	}

	pub unsafe fn dealloc_all(&mut self) {
		unsafe { self.dealloc_recurse(3); }
	}

	unsafe fn dealloc_recurse(&mut self, level: usize) {
		let last_entry_index = self.0.len() - 1;

		if level > 0 {
			for (i, pointer) in self.0.iter_mut().enumerate() {
				if pointer.flags().contains(PageTableFlags::HUGE) || (level == 3 && i == last_entry_index) {
					continue;
				}

                unsafe {
                    pointer.as_mut_ptr().as_mut()
                        .map(|page_table| page_table.dealloc_recurse(level-1));
                }
			}
		}

		unsafe { self.dealloc() }
	}

	pub fn add_entry(&mut self, index: usize, ptr: PageTablePointer) {
		assert!(!self.present(index));
		self.0[index] = ptr;
		self.inc_entry_count(1);
	}

	pub unsafe fn get(&mut self, index: usize) -> *mut PageTable {
		self.0[index].as_mut_ptr()
	}

	pub fn get_or_alloc<'a>(
		&'a mut self,
		index: usize,
		flags: PageTableFlags,
	) -> Option<&'a mut PageTable> {
		if self.present(index) {
			unsafe { self.0[index].as_mut_ptr().as_mut() }
		} else {
			let mut out = PageTable::new(flags)?;
			self.add_entry(index, out);
			unsafe { out.as_mut_ptr().as_mut() }
		}
	}

	pub fn remove(&mut self, index: usize) {
		if self.present(index) {
			self.0[index] = PageTablePointer(self.0[index].0 & !PageTableFlags::PRESENT.bits());
			self.inc_entry_count(-1);
		}
	}

	fn addr(&self) -> usize {
		self as *const _ as usize
	}
}
