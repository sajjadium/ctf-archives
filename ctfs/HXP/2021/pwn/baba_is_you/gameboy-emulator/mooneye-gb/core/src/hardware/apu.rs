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

use self::ch1::Ch1;
use self::ch2::Ch2;
use self::ch3::Ch3;
use self::ch4::Ch4;

mod ch1;
mod ch2;
mod ch3;
mod ch4;
mod envelope;
mod sweep;
mod wave_duty;

#[derive(Clone)]
pub struct Apu {
  enabled: bool,
  term1_volume: Volume,
  term2_volume: Volume,
  term1_vin: bool,
  term2_vin: bool,
  term1_channels: Channels,
  term2_channels: Channels,
  ch1: Ch1,
  ch2: Ch2,
  ch3: Ch3,
  ch4: Ch4,
  cycles: usize,
}

#[derive(Clone, Copy)]
enum Volume {
  Vol0 = 0x00,
  Vol1 = 0x01,
  Vol2 = 0x02,
  Vol3 = 0x03,
  Vol4 = 0x04,
  Vol5 = 0x05,
  Vol6 = 0x06,
  Vol7 = 0x07,
}

impl Volume {
  pub fn from_u8(value: u8) -> Option<Volume> {
    use self::Volume::*;
    match value {
      0x00 => Some(Vol0),
      0x01 => Some(Vol1),
      0x02 => Some(Vol2),
      0x03 => Some(Vol3),
      0x04 => Some(Vol4),
      0x05 => Some(Vol5),
      0x06 => Some(Vol6),
      0x07 => Some(Vol7),
      _ => None,
    }
  }
}

impl Apu {
  pub fn new() -> Apu {
    Apu {
      enabled: false,
      term1_volume: Volume::Vol0,
      term2_volume: Volume::Vol0,
      term1_vin: false,
      term2_vin: false,
      term1_channels: Channels::empty(),
      term2_channels: Channels::empty(),
      ch1: Ch1::new(),
      ch2: Ch2::new(),
      ch3: Ch3::new(),
      ch4: Ch4::new(),
      cycles: 4096,
    }
  }
  pub fn tick_cycle(&mut self) {
    if self.cycles > 0 {
      self.cycles -= 1;
    } else {
      self.cycles = 4096;
      self.ch1.clock();
      self.ch2.clock();
      self.ch3.clock();
      self.ch4.clock();
    }
  }
  pub fn nr10_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch1.sweep.read_reg()
  }
  pub fn nr10_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch1.sweep.write_reg(value);
    }
  }
  pub fn nr11_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch1.read_reg1()
  }
  pub fn nr11_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch1.write_reg1(value);
    }
  }
  pub fn nr12_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch1.envelope.read_reg()
  }
  pub fn nr12_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch1.envelope.write_reg(value);
    }
  }
  pub fn nr13_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    0xff
  }
  pub fn nr13_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch1.write_reg3(value);
    }
  }
  pub fn nr14_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch1.read_reg4()
  }
  pub fn nr14_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch1.write_reg4(value);
    }
  }
  pub fn nr21_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch2.read_reg1()
  }
  pub fn nr21_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch2.write_reg1(value);
    }
  }
  pub fn nr22_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch2.envelope.read_reg()
  }
  pub fn nr22_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch2.envelope.write_reg(value);
    }
  }
  pub fn nr23_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    0xff
  }
  pub fn nr23_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch2.write_reg3(value);
    }
  }
  pub fn nr24_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch2.read_reg4()
  }
  pub fn nr24_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch2.write_reg4(value);
    }
  }
  pub fn nr30_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch3.read_reg0()
  }
  pub fn nr30_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch3.write_reg0(value);
    }
  }
  pub fn nr31_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    0xff
  }
  pub fn nr31_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch3.write_reg1(value);
    }
  }
  pub fn nr32_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch3.read_reg2()
  }
  pub fn nr32_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch3.write_reg2(value);
    }
  }
  pub fn nr33_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    0xff
  }
  pub fn nr33_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch3.write_reg3(value);
    }
  }
  pub fn nr34_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch3.read_reg4()
  }
  pub fn nr34_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch3.write_reg4(value);
    }
  }
  pub fn nr41_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    0xff
  }
  pub fn nr41_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch4.write_reg1(value);
    }
  }
  pub fn nr42_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch4.envelope.read_reg()
  }
  pub fn nr42_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch4.envelope.write_reg(value);
    }
  }
  pub fn nr43_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch4.read_reg3()
  }
  pub fn nr43_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch4.write_reg3(value);
    }
  }
  pub fn nr44_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.ch4.read_reg4()
  }
  pub fn nr44_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.ch4.write_reg4(value);
    }
  }
  pub fn nr50_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.get_ctrl_volume()
  }
  pub fn nr50_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.set_ctrl_volume(value);
    }
  }
  pub fn nr51_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.get_terminal_channels()
  }
  pub fn nr51_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    if self.enabled {
      self.set_terminal_channels(value);
    }
  }
  pub fn nr52_read_cycle(&mut self) -> u8 {
    self.tick_cycle();
    self.get_ctrl_master()
  }
  pub fn nr52_write_cycle(&mut self, value: u8) {
    self.tick_cycle();
    self.set_ctrl_master(value);
  }
  pub fn wave_ram_read_cycle(&mut self, addr: u16) -> u8 {
    self.tick_cycle();
    self.ch3.read_wave_ram(addr - 0xff30)
  }
  pub fn wave_ram_write_cycle(&mut self, addr: u16, value: u8) {
    self.tick_cycle();
    self.ch3.write_wave_ram(addr - 0xff30, value);
  }

  pub fn get_terminal_channels(&self) -> u8 {
    self.term1_channels.bits | (self.term2_channels.bits << 4)
  }
  pub fn set_terminal_channels(&mut self, value: u8) {
    self.term1_channels = Channels::from_bits_truncate(value);
    self.term2_channels = Channels::from_bits_truncate(value >> 4);
  }
  pub fn get_ctrl_master(&self) -> u8 {
    const CTRL_MASTER_MASK: u8 = 0x70;

    CTRL_MASTER_MASK
      | if self.enabled { 1 << 7 } else { 0 }
      | if self.ch4.status { 1 << 3 } else { 0 }
      | if self.ch3.status { 1 << 2 } else { 0 }
      | if self.ch2.status { 1 << 1 } else { 0 }
      | if self.ch1.status { 1 << 0 } else { 0 }
  }
  pub fn set_ctrl_master(&mut self, value: u8) {
    self.enabled = value & (1 << 7) != 0;
    if !self.enabled {
      self.ch1.reset();
      self.ch2.reset();
      self.ch3.reset();
      self.ch4.reset();
      self.term1_volume = Volume::Vol0;
      self.term2_volume = Volume::Vol0;
      self.term1_vin = false;
      self.term2_vin = false;
      self.term1_channels = Channels::empty();
      self.term2_channels = Channels::empty();
    }
  }
  pub fn get_ctrl_volume(&self) -> u8 {
    (self.term1_volume as u8)
      | if self.term1_vin { 1 << 3 } else { 0 }
      | (self.term2_volume as u8) << 4
      | if self.term2_vin { 1 << 7 } else { 0 }
  }
  pub fn set_ctrl_volume(&mut self, value: u8) {
    self.term1_volume = Volume::from_u8(value & 0x07).unwrap();
    self.term1_vin = value & (1 << 3) != 0;
    self.term2_volume = Volume::from_u8((value >> 4) & 0x07).unwrap();
    self.term2_vin = value & (1 << 7) != 0;
  }
}

bitflags!(
  struct Channels: u8 {
    const CH_1 = 1 << 0;
    const CH_2 = 1 << 1;
    const CH_3 = 1 << 2;
    const CH_4 = 1 << 3;
  }
);
