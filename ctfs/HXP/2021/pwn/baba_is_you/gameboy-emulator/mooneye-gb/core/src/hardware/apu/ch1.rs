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
use super::sweep::Sweep;
use super::wave_duty::WaveDuty;

#[derive(Clone)]
pub struct Ch1 {
  pub sweep: Sweep,
  wave_duty: WaveDuty,
  pub envelope: Envelope,
  freq_bits: u16,
  use_counter: bool,
  counter: usize,
  pub status: bool,
}

impl Ch1 {
  pub fn new() -> Ch1 {
    Ch1 {
      sweep: Sweep::new(),
      wave_duty: WaveDuty::HalfQuarter,
      envelope: Envelope::new(),
      freq_bits: 0,
      use_counter: false,
      counter: 0,
      status: false,
    }
  }
  pub fn reset(&mut self) {
    *self = Ch1::new();
  }
  pub fn read_reg1(&self) -> u8 {
    const REG1_MASK: u8 = 0x3F;

    REG1_MASK | ((self.wave_duty as u8) << 6)
  }
  pub fn write_reg1(&mut self, value: u8) {
    self.wave_duty = WaveDuty::from_u8((value >> 6) & 0x03).unwrap();
    self.counter = 64 - (value & 0x3f) as usize;
  }
  pub fn write_reg3(&mut self, value: u8) {
    self.freq_bits = (self.freq_bits & 0x700) | value as u16;
  }
  pub fn read_reg4(&self) -> u8 {
    const REG4_MASK: u8 = 0xBF;

    REG4_MASK | if self.use_counter { 1 << 6 } else { 0 }
  }
  pub fn write_reg4(&mut self, value: u8) {
    self.status = value & (1 << 7) != 0;
    self.use_counter = value & (1 << 6) != 0;
    self.freq_bits = (self.freq_bits & 0xff) | ((value as u16) << 8);
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
