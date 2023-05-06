#![no_std]
#![no_main]
#![feature(maybe_uninit_uninit_array)]
#![feature(array_methods)]
#![feature(alloc_error_handler)]
#![feature(allocator_api)]
#![feature(stmt_expr_attributes)]
#![feature(const_mut_refs)]
#![feature(bound_map)]
#![feature(slice_index_methods)]
#![feature(slice_ptr_len)]
#![feature(slice_ptr_get)]
#![feature(dropck_eyepatch)]
#![feature(ptr_metadata)]
#![feature(let_chains)]
#![feature(try_blocks)]
#![feature(return_position_impl_trait_in_trait)]
#![deny(unsafe_op_in_unsafe_fn)]
#![feature(custom_test_frameworks)]
#![test_runner(crate::test_runner)]
#![reexport_test_harness_main = "test_main"]

extern crate alloc;

mod allocation;
mod arch;
mod int;
mod mem;
mod sched;
mod util;
mod vmem_manager;

mod consts;
mod gdt;
mod gs_data;
mod io;
mod linked_list;
mod mb2;
mod prelude;
mod sync;
mod syscall;
mod syserr;

use core::panic::PanicInfo;
use core::cmp::min;

use allocation::alloc_at;
use arch::x64::*;
use consts::INIT_STACK;
use mb2::BootInfo;
use prelude::*;
use sched::create_thread;
use vmem_manager::PageMappingFlags;

static FLAG: &'static str = "bctf{REDACTED_REDACTED_REDACTED_REDACTED_REDACTED_REDAC}";

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    println!("{}", info);

    loop {
        cli();
        hlt();
    }
}

fn init(boot_info_addr: usize) -> KResult<()> {
    io::init();

    let boot_info = unsafe { BootInfo::new(boot_info_addr) };

    unsafe {
        allocation::init(&boot_info.memory_map)?;
    }

    gs_data::init();

    gdt::init();

    int::init();

    vmem_manager::init();

    syscall::init();

    sched::init(*INIT_STACK)?;

    Ok(())
}

fn load_user_code() -> KResult<()> {
    println!("loading user code...");

    let code_zone = AVirtRange::new(VirtAddr::new(0x40000), PAGE_SIZE * 4);
    let stack_zone = AVirtRange::new(VirtAddr::new(0x10000), PAGE_SIZE * 4);

    alloc_at(code_zone, PageMappingFlags::READ | PageMappingFlags::EXEC | PageMappingFlags::USER)
        .expect("could not allocate user code zone");

    alloc_at(stack_zone, PageMappingFlags::READ | PageMappingFlags::WRITE | PageMappingFlags::USER)
        .expect("could not allocate user stack zone");

    let mut serial_port = io::SERIAL_PORT.lock();

    let num_bytes = serial_port.receive() as usize
        | ((serial_port.receive() as usize) << 8);
    let num_bytes = min(code_zone.size(), num_bytes);

    let code_slice = unsafe { code_zone.as_slice_mut() };

    for i in 0..num_bytes {
        code_slice[i] = serial_port.receive();
    }

    drop(serial_port);

    create_thread(code_zone.as_usize(), stack_zone.end_usize())
        .expect("could not create user thread");

    println!("loaded {} bytes of code", num_bytes);

    Ok(())
}

#[no_mangle]
pub extern "C" fn _start(boot_info_addr: usize) -> ! {
    println!("{}", FLAG.len());

    init(boot_info_addr).expect("kernel init failed");

    load_user_code().expect("failed to load user code");

    sti();

    loop {
        hlt();
    }
}

#[cfg(test)]
fn test_runner(tests: &[&dyn Fn()]) {
    println!("Running {} tests", tests.len());
    for test in tests {
        test();
    }
    println!("All tests passed");
}

#[test_case]
fn test() {}