// This file is part of Mooneye GB.
// Copyright (C) 2014-2020 Joonas Javanainen <joonas.javanainen@gmail.com>
//
// Mooneye GB is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Mooneye GB is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Mooneye GB.  If not, see <http://www.gnu.org/licenses/>.
use bitflags::bitflags;

use crate::util::int::IntExt;

bitflags!(
  pub struct InterruptLine: u8 {
    const VBLANK = 1 << 0;
    const STAT = 1 << 1;
    const TIMER = 1 << 2;
    const SERIAL = 1 << 3;
    const JOYPAD = 1 << 4;
  }
);

impl InterruptLine {
  pub fn highest_priority(&self) -> InterruptLine {
    InterruptLine::from_bits_truncate(self.bits().isolate_rightmost_one())
  }
}

pub trait InterruptRequest {
  fn request_t12_interrupt(&mut self, interrupt: InterruptLine);
  fn request_t34_interrupt(&mut self, interrupt: InterruptLine);
}

impl InterruptRequest for InterruptLine {
  fn request_t12_interrupt(&mut self, interrupt: InterruptLine) {
    *self |= interrupt;
  }
  fn request_t34_interrupt(&mut self, interrupt: InterruptLine) {
    *self |= interrupt;
  }
}

#[derive(Clone, Debug)]
pub struct Interrupts {
  intr_flags: InterruptLine,
  intr_enable: u8,
}

impl Interrupts {
  pub fn new() -> Interrupts {
    Interrupts {
      intr_flags: InterruptLine::empty(),
      intr_enable: 0x00,
    }
  }
  pub fn get_interrupt_flag(&self) -> u8 {
    const IF_UNUSED_MASK: u8 = (1 << 5) | (1 << 6) | (1 << 7);

    self.intr_flags.bits() | IF_UNUSED_MASK
  }
  pub fn get_interrupt_enable(&self) -> u8 {
    self.intr_enable
  }
  pub fn set_interrupt_flag(&mut self, value: u8) {
    self.intr_flags = InterruptLine::from_bits_truncate(value);
  }
  pub fn set_interrupt_enable(&mut self, value: u8) {
    self.intr_enable = value;
  }
  pub fn get_interrupt(&self) -> InterruptLine {
    self.intr_flags & InterruptLine::from_bits_truncate(self.intr_enable)
  }
  pub fn ack_interrupt(&mut self, mask: InterruptLine) {
    self.intr_flags -= mask;
  }
}

impl InterruptRequest for Interrupts {
  fn request_t12_interrupt(&mut self, interrupt: InterruptLine) {
    self.intr_flags |= interrupt;
  }
  fn request_t34_interrupt(&mut self, interrupt: InterruptLine) {
    self.intr_flags |= interrupt;
  }
}
