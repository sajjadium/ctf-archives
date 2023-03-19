use crate::allocation::{alloc_at, dealloc_at};
use crate::arch::x64::IntDisable;
use crate::prelude::*;
use crate::io::SERIAL_PORT;
use crate::sched::{create_thread, switch_current_thread_to, PostSwitchAction, ThreadState};
use crate::vmem_manager::PageMappingFlags;

pub fn print_debug(
    options: u32,
    a1: usize,
    a2: usize,
    a3: usize,
    a4: usize,
    a5: usize,
    a6: usize,
    a7: usize,
    a8: usize,
    a9: usize,
    a10: usize,
) -> KResult<()> {
	let mut writer = SERIAL_PORT.lock();
	
	let mut print_bytes = |bytes, mut n| {
		let mut i = 0;
		while i < core::mem::size_of::<usize>() && n > 0 {
			writer.send(get_bits(bytes, (8 * i)..(8 * i + 8)) as u8);
			i += 1;
			n -= 1;
		}
		n
	};

	let mut n = core::cmp::min(options, 80) as usize;
	n = print_bytes(a1, n);
	n = print_bytes(a2, n);
	n = print_bytes(a3, n);
	n = print_bytes(a4, n);
	n = print_bytes(a5, n);
	n = print_bytes(a6, n);
	n = print_bytes(a7, n);
	n = print_bytes(a8, n);
	n = print_bytes(a9, n);
	print_bytes(a10, n);

    Ok(())
}

pub fn alloc(
	options: u32,
	address: usize,
	size: usize,
) -> KResult<()> {
	let flags = PageMappingFlags::from_bits_truncate(options as usize)
		| PageMappingFlags::USER;
	
	let address = VirtAddr::try_new(address)
		.ok_or(SysErr::InvlVirtAddr)?;
	
	let range = AVirtRange::try_new_aligned(address, size)
		.ok_or(SysErr::InvlAlign)?;
	
	alloc_at(range, flags)
}

pub fn dealloc(
	_options: u32,
	address: usize,
) -> KResult<()> {
	let address = VirtAddr::try_new(address)
		.ok_or(SysErr::InvlVirtAddr)?;

	dealloc_at(address)
}

pub fn thread_new(
	_options: u32,
	rip: usize,
	rsp: usize,
) -> KResult<()> {
	create_thread(rip, rsp)
}

pub fn thread_yield(_options: u32) -> KResult<()> {
	switch_current_thread_to(ThreadState::Ready, IntDisable::new(), PostSwitchAction::None)
		.expect("failed to yield thread");

	Ok(())
}

pub fn thread_destroy(_options: u32) -> KResult<()> {
	switch_current_thread_to(ThreadState::Dead, IntDisable::new(), PostSwitchAction::None)
		.expect("failed to destroy thread");

	Ok(())
}

pub fn shutdown(_options: u32) -> KResult<()> {
	println!("shutting down...");
	
	unsafe {
		core::arch::asm!(
			"mov al, 0xfe\nout 0x64, al",
			out("rax") _,
		);
	}

	Ok(())
}