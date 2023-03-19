use crate::prelude::*;
use crate::arch::x64::{
	rdmsr, wrmsr, EFER_MSR, EFER_SYSCALL_ENABLE, FMASK_MSR, LSTAR_MSR, STAR_MSR,
};

mod calls;
use calls::*;

extern "C" {
    fn syscall_entry();
}

#[derive(Debug)]
#[repr(C)]
pub struct SyscallVals {
    pub options: u32,
	unused: u32,
	pub a1: usize,
	pub a2: usize,
	pub a3: usize,
	pub a4: usize,
	pub a5: usize,
	pub a6: usize,
	pub a7: usize,
	pub a8: usize,
	pub a9: usize,
	pub a10: usize,
	pub rsp: usize,
	pub rflags: usize,
    pub rip: usize,
}

macro_rules! syscall_0 {
	($func:expr, $vals:expr) => {
		$func($vals.options)
	};
}

macro_rules! syscall_1 {
	($func:expr, $vals:expr) => {
		$func(
			$vals.options,
			$vals.a1,
		)
	};
}

macro_rules! syscall_2 {
	($func:expr, $vals:expr) => {
		$func(
			$vals.options,
			$vals.a1,
			$vals.a2,
		)
	};
}

macro_rules! sysret_0 {
	($ret:expr, $vals:expr) => {
		match $ret {
			Ok(()) => $vals.a1 = SysErr::Ok.num(),
			Err(err) => $vals.a1 = err.num(),
		}
	};
}

pub const PRINT_DEBUG: u32 = 0;

pub const ALLOC: u32 = 1;
pub const DEALLOC: u32 = 2;

pub const THREAD_NEW: u32 = 3;
pub const THREAD_YIELD: u32 = 4;
pub const THREAD_DESTROY: u32 = 5;

pub const SHUTDOWN: u32 = 6;

#[no_mangle]
extern "C" fn rust_syscall_entry(syscall_num: u32, vals: &mut SyscallVals) {
    match syscall_num {
		PRINT_DEBUG => sysret_0!(print_debug(
			vals.options,
			vals.a1,
			vals.a2,
			vals.a3,
			vals.a4,
			vals.a5,
			vals.a6,
			vals.a7,
			vals.a8,
			vals.a9,
			vals.a10,
		), vals),
		ALLOC => sysret_0!(syscall_2!(alloc, vals), vals),
		DEALLOC => sysret_0!(syscall_1!(dealloc, vals), vals),
		THREAD_NEW => sysret_0!(syscall_2!(thread_new, vals), vals),
		THREAD_YIELD => sysret_0!(syscall_0!(thread_yield, vals), vals),
		THREAD_DESTROY => sysret_0!(syscall_0!(thread_destroy, vals), vals),
		SHUTDOWN => sysret_0!(syscall_0!(shutdown, vals), vals),
        _ => vals.a1 = SysErr::InvlSyscall.num(),
    }
}

pub fn init() {
    let efer = rdmsr(EFER_MSR);
	wrmsr(EFER_MSR, efer | EFER_SYSCALL_ENABLE);

	wrmsr(LSTAR_MSR, syscall_entry as usize as u64);

	wrmsr(FMASK_MSR, 0x200);

	wrmsr(STAR_MSR, 0x0013000800000000);
}