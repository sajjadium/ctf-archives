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
use super::envelope::Envelope;

#[derive(Clone)]
pub struct Ch4 {
  pub envelope: Envelope,
  noise_opt: u8,
  use_counter: bool,
  counter: usize,
  pub status: bool,
}

impl Ch4 {
  pub fn new() -> Ch4 {
    Ch4 {
      envelope: Envelope::new(),
      noise_opt: 0,
      use_counter: false,
      counter: 0,
      status: false,
    }
  }
  pub fn reset(&mut self) {
    *self = Ch4::new()
  }
  pub fn write_reg1(&mut self, value: u8) {
    self.counter = 64 - (value & 0x3f) as usize;
  }
  pub fn read_reg3(&self) -> u8 {
    self.noise_opt
  }
  pub fn write_reg3(&mut self, value: u8) {
    self.noise_opt = value
  }
  pub fn read_reg4(&self) -> u8 {
    const REG4_MASK: u8 = 0xbf;

    REG4_MASK | if self.use_counter { 1 << 6 } else { 0 }
  }
  pub fn write_reg4(&mut self, value: u8) {
    self.status = value & (1 << 7) != 0;
    self.use_counter = value & (1 << 6) != 0;
    if self.status && self.counter == 0 {
      self.counter = 64;
    }
  }
  pub fn clock(&mut self) {
    if self.use_counter && self.counter > 0 {
      self.counter -= 1;

      if self.counter == 0 {
        self.status = false;
      }
    }
  }
}
