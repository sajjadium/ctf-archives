use core::fmt;

pub struct UART {
    sr: u32,
    dr: u32,
    _a: u32,
    cr1: u32,
}

impl UART {
    pub fn new() -> &'static mut UART {
        let uart = unsafe { &mut *(0x40011000 as *mut UART) };
        uart.cr1 = (1 << 13) | (1 << 3) | (1 << 2);
        uart
    }

    pub fn receive_byte(&self) -> u8 {
        while unsafe { core::ptr::read_volatile(&self.sr as *const u32) } & (1 << 5) == 0 {}
        return (unsafe { core::ptr::read_volatile(&self.dr as *const u32) } & 0xffu32) as u8;
    }
}

// From Stack Overflow
// https://stackoverflow.com/questions/39488327/how-to-format-output-to-a-byte-array-with-no-std-and-no-allocator
impl fmt::Write for UART {
    fn write_str(&mut self, s: &str) -> fmt::Result {
        for c in s.bytes() {
            unsafe { core::ptr::write_volatile(&mut self.dr as *mut u32, c as u32) };
        }
        Ok(())
    }
}

pub fn _print(args: fmt::Arguments) {
    use core::fmt::Write;
    UART::new().write_fmt(args).unwrap();
}

#[macro_export]
macro_rules! print {
    ($($arg:tt)*) => {
        ($crate::uart::_print(format_args!($($arg)*)))
    }
}

#[macro_export]
macro_rules! println {
    () => ($crate::print!("\n"));
    ($($arg:tt)*) => ($crate::print!("{}\n", format_args!($($arg)*)));
}
