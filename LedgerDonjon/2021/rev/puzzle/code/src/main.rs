#![no_std]
#![no_main]
#![feature(asm)]

mod qemu;
mod reset;
mod uart;
use core::cell::RefCell;

struct RefCellWrapper<T>(pub RefCell<T>);

unsafe impl<T> Sync for RefCellWrapper<T> {}

use core::ops::Deref;
impl<T> Deref for RefCellWrapper<T> {
    type Target = RefCell<T>;
    fn deref(&self) -> &RefCell<T> {
        &self.0
    }
}

#[link_section = ".mainbuffer"]
static BUFFER: RefCellWrapper<[u8; 32]> = RefCellWrapper(RefCell::new([0u8; 32]));

#[repr(C)]
struct AdminParams {
    serial: [u8; 16],
    device_name: [u8; 10],
    debug_mode: bool,
    interrupt_init: u32,
}

#[link_section = ".config"]
static CONFIG: RefCellWrapper<AdminParams> = RefCellWrapper(RefCell::new(AdminParams {
    serial: [0; 16],
    device_name: [0; 10],
    debug_mode: false,
    interrupt_init: 0u32,
}));

fn init() {
    let mut config = CONFIG.borrow_mut();
    config.serial = [0xd7; 16];
    config.device_name = *b"PuzzleTime";
}

fn init_vtor() {
    let new_vtor = CONFIG.borrow().interrupt_init;
    if new_vtor <= 0x2000_0000 {
        unsafe { core::ptr::write_volatile(0xE000ED08 as *mut u32, new_vtor) };
    }
}

#[link_section = ".welcome"]
#[inline(never)]
fn print_welcome() {
    let lr = reset::__get_lr();

    println!("--- Welcome to Donjon services ---");

    if lr & 0xfffffff0 == 0xfffffff0 {
        qemu::dump_flag();
        qemu::exit();
    }
}

fn recv() {
    print!("Command: ");
    let uart = uart::UART::new();

    let mut buffer = BUFFER.borrow_mut();
    for b in buffer.iter_mut() {
        let byte = uart.receive_byte();
        print!("{}", byte as char);
        if byte == b'\n' as u8 {
            break;
        } else {
            *b = byte;
        }
    }
    print!("\n");
}

fn recv_and_exec_cmd() {
    recv();

    let buffer = BUFFER.borrow();
    let opcode = buffer[0];

    match opcode {
        0x30 => print_welcome(),
        0x31 => {
            if CONFIG.borrow().debug_mode {
                init_vtor();
            } else {
                println!("Not in DEBUG mode.");
            }
        }
        _ => println!("Unknown command"),
    }
}

#[no_mangle]
pub fn _start() {
    init();
    init_vtor();

    recv_and_exec_cmd();
    recv_and_exec_cmd();
}
