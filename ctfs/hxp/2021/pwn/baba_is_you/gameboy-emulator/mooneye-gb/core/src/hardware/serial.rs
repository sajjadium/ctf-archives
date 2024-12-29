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

#[derive(Clone)]
pub struct Serial {
  data: u8,
  control: Control,
}

impl Serial {
  pub fn new() -> Serial {
    Serial {
      data: 0x00,
      control: Control::empty(),
    }
  }
  pub fn get_data(&self) -> u8 {
    self.data
  }
  pub fn set_data(&mut self, value: u8) {
    self.data = value
  }
  pub fn get_control(&self) -> u8 {
    self.control.bits | CTRL_UNUSED_MASK
  }
  pub fn set_control(&mut self, value: u8) {
    self.control = Control::from_bits_truncate(value);
    if self.control.contains(Control::START) {
      // println!("Serial transfer {:02x} {}, control = {:08b}", self.data, char::from_u32(self.data as u32).unwrap_or('?'), self.control.bits);
    }
  }
}

const CTRL_UNUSED_MASK: u8 = (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6);

bitflags!(
  struct Control: u8 {
    const CLOCK = 1 << 0;
    const START = 1 << 7;
  }
);
