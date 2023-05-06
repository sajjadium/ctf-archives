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
#[derive(Clone, Copy)]
enum Volume {
  None = 0,
  Full = 1,
  Half = 2,
  Quarter = 3,
}

impl Volume {
  pub fn from_u8(value: u8) -> Option<Volume> {
    use self::Volume::*;
    match value {
      0 => Some(None),
      1 => Some(Full),
      2 => Some(Half),
      3 => Some(Quarter),
      _ => Option::None,
    }
  }
}

#[derive(Clone)]
pub struct Ch3 {
  wave_ram: [u8; 16],
  enabled: bool,
  volume: Volume,
  freq_bits: u16,
  use_counter: bool,
  counter: usize,
  pub status: bool,
}

impl Ch3 {
  pub fn new() -> Ch3 {
    Ch3 {
      wave_ram: [0; 16],
      enabled: false,
      volume: Volume::None,
      freq_bits: 0,
      use_counter: false,
      counter: 0,
      status: false,
    }
  }
  pub fn reset(&mut self) {
    self.enabled = false;
    self.volume = Volume::None;
    self.use_counter = false;
    self.counter = 0;
    self.status = false;
  }
  pub fn read_wave_ram(&self, reladdr: u16) -> u8 {
    self.wave_ram[reladdr as usize]
  }
  pub fn write_wave_ram(&mut self, reladdr: u16, value: u8) {
    self.wave_ram[reladdr as usize] = value;
  }
  pub fn read_reg0(&self) -> u8 {
    const REG0_MASK: u8 = 0x7f;

    REG0_MASK | if self.enabled { 1 << 7 } else { 0 }
  }
  pub fn write_reg0(&mut self, value: u8) {
    self.enabled = value & (1 << 7) != 0;
  }
  pub fn write_reg1(&mut self, value: u8) {
    self.counter = 256 - value as usize;
  }
  pub fn read_reg2(&self) -> u8 {
    const REG2_MASK: u8 = 0x9f;

    REG2_MASK | ((self.volume as u8) << 5)
  }
  pub fn write_reg2(&mut self, value: u8) {
    self.volume = Volume::from_u8((value >> 5) & 0x03).unwrap();
  }
  pub fn write_reg3(&mut self, value: u8) {
    self.freq_bits = (self.freq_bits & 0x700) | value as u16;
  }
  pub fn read_reg4(&self) -> u8 {
    const REG4_MASK: u8 = 0xbf;

    REG4_MASK | if self.use_counter { 1 << 6 } else { 0 }
  }
  pub fn write_reg4(&mut self, value: u8) {
    self.status = value & (1 << 7) != 0;
    self.use_counter = value & (1 << 6) != 0;
    self.freq_bits = (self.freq_bits & 0xff) | ((value as u16) << 8);
    if self.status && self.counter == 0 {
      self.counter = 256;
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
