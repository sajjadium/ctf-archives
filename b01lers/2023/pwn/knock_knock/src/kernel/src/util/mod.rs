
use core::arch::asm;
use core::ops::Range;
use core::str::Utf8Error;

use crate::prelude::*;

mod hwa_iter;

pub use hwa_iter::*;

pub const fn align_up(addr: usize, align: usize) -> usize {
    (addr + align - 1) & !(align - 1)
}

pub const fn align_down(addr: usize, align: usize) -> usize {
    addr & !(align - 1)
}

pub fn align_of(addr: usize) -> usize {
    if addr == 0 {
        return 1 << 63;
    }

    let out: usize;

    unsafe {
        asm!("bsf {}, {}",
			out(reg) out,
			in(reg) addr);
    }

    1 << out
}

pub fn page_aligned(addr: usize) -> bool {
    align_of(addr) >= PAGE_SIZE
}

pub const fn get_bits(n: usize, bits: Range<usize>) -> usize {
    if bits.end == 0 {
        return 0;
    }

    let l = if bits.start > 63 { 63 } else { bits.start };
    let h = if bits.end > 64 { 63 } else { bits.end - 1 };
    if l > h {
        return 0;
    }

    let temp = if h == 63 { usize::MAX } else { (1 << (h + 1)) - 1 };

    (temp & n).wrapping_shr(l as _)
}

pub const fn get_bits_raw(n: usize, bits: Range<usize>) -> usize {
    let l = if bits.start > 63 { 63 } else { bits.start };
    let h = if bits.end > 63 { 63 } else { bits.end };
    if l >= h {
        return 0;
    }

    let temp = if h == 63 { usize::MAX } else { (1 << (h + 1)) - 1 };

    (temp & n).wrapping_shr(l as _) << l
}

pub unsafe fn memset(mem: *mut u8, len: usize, data: u8) {
    for i in 0..len {
        unsafe {
            *mem.add(i) = data;
        }
    }
}

#[inline]
pub fn log2(n: usize) -> usize {
    if n == 0 {
        return 0;
    }

    let out;

    unsafe {
        asm!("bsr {}, {}",
			out(reg) out,
			in(reg) n);
    }

    out
}

pub fn log2_up(n: usize) -> usize {
    if n == 1 {
        1
    } else {
        log2(align_up(n, 1 << log2(n)))
    }
}

pub const fn log2_const(n: usize) -> usize {
    if n == 0 {
        return 0;
    }

    let mut out = 0;
    while get_bits(n, out..64) > 0 {
        out += 1;
    }

    out - 1
}

pub const fn log2_up_const(n: usize) -> usize {
    if n == 1 {
        1
    } else {
        log2_const(align_up(n, 1 << log2_const(n)))
    }
}

pub unsafe fn unbound_mut<'a, 'b, T>(r: &'a mut T) -> &'b mut T {
    unsafe { (r as *mut T).as_mut().unwrap() }
}

pub fn aligned_nonnull<T>(ptr: *const T) -> bool {
    core::mem::align_of::<T>() == align_of(ptr as usize) && !ptr.is_null()
}

pub unsafe fn from_cstr<'a>(ptr: *const u8) -> Result<&'a str, Utf8Error> {
    let mut len = 0;
    let start = ptr;

    loop {
        if unsafe { *ptr.add(len) } != 0 {
            len += 1;
        } else {
            break;
        }
    }

    unsafe {
        let slice = core::slice::from_raw_parts(start, len);
        core::str::from_utf8(slice)
    }
}

#[macro_export]
macro_rules! init_array (
	($ty:ty, $len:expr, $val:expr) => (
		{
			use core::mem::MaybeUninit;
			let mut array: [MaybeUninit<$ty>; $len] = MaybeUninit::uninit_array();
			for a in array.iter_mut() {
				#[allow(unused_unsafe)]
				unsafe { ::core::ptr::write(a.as_mut_ptr(), $val); }
			}
			#[allow(unused_unsafe)]
			unsafe { core::mem::transmute::<[MaybeUninit<$ty>; $len], [$ty; $len]>(array) }
		}
	)
);