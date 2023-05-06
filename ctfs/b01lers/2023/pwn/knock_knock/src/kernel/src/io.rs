use core::fmt::{self, Write};

use uart_16550::SerialPort;

use crate::sync::IMutex;

pub static SERIAL_PORT: IMutex<SerialPort> = unsafe { IMutex::new(SerialPort::new(0x3f8)) };

#[macro_export]
macro_rules! print {
	($($arg:tt)*) => ($crate::io::_print(format_args!($($arg)*)));
}

#[macro_export]
macro_rules! println {
	() => ($crate::print!("\n"));
	($($arg:tt)*) => ($crate::print!("{}\n", format_args!($($arg)*)));
}

#[doc(hidden)]
pub fn _print(args: fmt::Arguments) {
    SERIAL_PORT.lock().write_fmt(args).unwrap();
}

pub fn init() {
    SERIAL_PORT.lock().init();
}