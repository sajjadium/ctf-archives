use core::sync::atomic::{AtomicU64, AtomicU16, Ordering};

use spin::Once;

use crate::prelude::*;
use crate::arch::x64::*;
use crate::sync::IMutex;

const PIT_INTERRUPT_TERMINAL_COUNT: u8 = 0;
const PIT_ONE_SHOT: u8 = 1;
const PIT_RATE_GENERATOR: u8 = 2;
const PIT_SQUARE_WAVE: u8 = 3;
const PIT_SOFTWARE_STROBE: u8 = 4;
const PIT_HARDWARE_STROBE: u8 = 5;

const PIT_CHANNEL_0: u16 = 0x40;
const PIT_CHANNEL_1: u16 = 0x41;
const PIT_CHANNEL_2: u16 = 0x42;
const PIT_COMMAND: u16 = 0x43;

const NANOSEC_PER_CLOCK: u64 = 838;

pub static PIT: Once<Pit> = Once::new();

pub struct Pit {
	elapsed_time: AtomicU64,
	reset: AtomicU16,
	nano_reset: AtomicU64,
	lock: IMutex<()>,
}

impl Pit {
	pub fn new(reset: u16) -> Self {
		let out = Pit {
			elapsed_time: AtomicU64::new(0),
			reset: AtomicU16::new(0),
			nano_reset: AtomicU64::new(0),
			lock: IMutex::new(()),
		};
		out.set_reset(reset);
		out
	}

	pub fn set_reset(&self, ticks: u16) {
		let _lock = self.lock.lock();
		outb(PIT_COMMAND, 0b00110100);
		outb(PIT_CHANNEL_0, get_bits(ticks as _, 0..8) as _);
		outb(PIT_CHANNEL_0, get_bits(ticks as _, 8..16) as _);

		self.reset.store(ticks, Ordering::Release);
		self.nano_reset.store(NANOSEC_PER_CLOCK * ticks as u64, Ordering::Release);
	}

	pub fn nsec(&self) -> u64 {
		if let Some(_lock) = self.lock.try_lock() {
			outb(PIT_COMMAND, 0);
			let low = inb(PIT_CHANNEL_0);
			let high = inb(PIT_CHANNEL_0);
			self.elapsed_time.load(Ordering::Relaxed)
				+ (NANOSEC_PER_CLOCK
					* (self.reset.load(Ordering::Relaxed) as u64
						- ((high as u64) << 8 | low as u64)))
		} else {
			self.nsec_no_latch()
		}
	}

	pub fn nsec_no_latch(&self) -> u64 {
		self.elapsed_time.load(Ordering::Acquire)
	}

	pub fn disable(&self) {
		let _lock = self.lock.lock();
		outb(PIT_COMMAND, 0b00110010);
	}

	pub fn irq_handler(&self) {
		self.elapsed_time.fetch_add(self.nano_reset.load(Ordering::Acquire), Ordering::AcqRel);
	}
}
