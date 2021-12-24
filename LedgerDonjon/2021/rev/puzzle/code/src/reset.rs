use crate::qemu::exit;

pub fn default_handler() -> ! {
    exit();
}

#[inline(always)]
pub fn __get_lr() -> u32 {
    let lr: u32;
    unsafe {
        asm!("mov {}, lr", out(reg) lr);
    }
    lr
}

pub fn hf_handler() -> ! {
    crate::println!("[!] HardFault hit, shutting down...");
    exit();
}

#[link_section = ".vectort"]
#[used]
pub static VECTOR_INIT_TABLE: [fn() -> !; 2] = [default_handler, hf_handler];
