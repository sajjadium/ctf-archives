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
use crate::config;
use crate::gameboy::{RAM_BANK_SIZE, ROM_BANK_SIZE};
use crate::util::int::IntExt;
use std::sync::Arc;

#[derive(Debug, Clone)]
struct Mbc1State {
  ramg: bool,
  bank1: u8,
  bank2: u8,
  mode: bool,
}

impl Default for Mbc1State {
  fn default() -> Mbc1State {
    Mbc1State {
      ramg: false,
      bank1: 0b0_0001,
      bank2: 0b00,
      mode: false,
    }
  }
}

impl Mbc1State {
  fn rom_offsets(&self, multicart: bool) -> (usize, usize) {
    let upper_bits = if multicart {
      self.bank2 << 4
    } else {
      self.bank2 << 5
    };
    let lower_bits = if multicart {
      self.bank1 & 0b1111
    } else {
      self.bank1
    };

    let lower_bank = if self.mode { upper_bits as usize } else { 0b00 };
    let upper_bank = (upper_bits | lower_bits) as usize;
    (ROM_BANK_SIZE * lower_bank, ROM_BANK_SIZE * upper_bank)
  }
  fn ram_offset(&self) -> usize {
    let bank = if self.mode { self.bank2 as usize } else { 0b00 };
    RAM_BANK_SIZE * bank
  }
}

#[derive(Debug, Clone)]
struct Mbc2State {
  ramg: bool,
  rom_bank: u8,
}

impl Default for Mbc2State {
  fn default() -> Mbc2State {
    Mbc2State {
      ramg: false,
      rom_bank: 0b0001,
    }
  }
}

#[derive(Debug, Clone)]
struct Mbc3State {
  rom_bank: u8,
  map_en: bool,
  map_select: u8,
}

impl Default for Mbc3State {
  fn default() -> Mbc3State {
    Mbc3State {
      rom_bank: 0b0000_0001,
      map_en: false,
      map_select: 0b0000,
    }
  }
}

#[derive(Debug, Clone)]
struct Mbc5State {
  ramg: bool,
  romb0: u8,
  romb1: u8,
  ramb: u8,
}

impl Default for Mbc5State {
  fn default() -> Mbc5State {
    Mbc5State {
      ramg: false,
      romb0: 0b0000_0001,
      romb1: 0b0,
      ramb: 0b0000,
    }
  }
}

impl Mbc5State {
  fn rom_offsets(&self) -> (usize, usize) {
    let lower_bits = self.romb0 as usize;
    let upper_bits = (self.romb1 as usize) << 8;
    let rom_bank = upper_bits | lower_bits;
    (0x0000, ROM_BANK_SIZE * rom_bank)
  }
}

#[derive(Debug, Clone)]
struct Huc1State {
  mode: u8,
  rom_bank: u8,
  ram_bank: u8,
}

impl Default for Huc1State {
  fn default() -> Huc1State {
    Huc1State {
      mode: 0b0000,
      rom_bank: 0b00_0000,
      ram_bank: 0b00,
    }
  }
}

#[derive(Debug, Clone)]
enum Mbc {
  None,
  Mbc1 { state: Mbc1State, multicart: bool },
  Mbc2 { state: Mbc2State },
  Mbc3 { state: Mbc3State, mbc30: bool },
  Mbc5 { state: Mbc5State },
  Huc1 { state: Huc1State },
}

impl Mbc {
  fn from_config(config: &config::Cartridge) -> Mbc {
    use config::CartridgeType::*;
    match config.cartridge_type {
      NoMbc { .. } => Mbc::None,
      Mbc1 { multicart, .. } => Mbc::Mbc1 {
        multicart,
        state: Mbc1State::default(),
      },
      Mbc2 { .. } => Mbc::Mbc2 {
        state: Mbc2State::default(),
      },
      Mbc3 { .. } => Mbc::Mbc3 {
        mbc30: config.ram_size.as_usize() > 65536,
        state: Mbc3State::default(),
      },
      Mbc5 { .. } => Mbc::Mbc5 {
        state: Mbc5State::default(),
      },
      Huc1 { .. } => Mbc::Huc1 {
        state: Huc1State::default(),
      },
      _ => panic!("Unsupported cartridge type {:?}", config.cartridge_type),
    }
  }
}

#[derive(Clone)]
pub struct Cartridge {
  mbc: Mbc,
  rom: Arc<[u8]>,
  rom_offsets: (usize, usize),
  ram: Box<[u8]>,
  ram_offset: usize,
}

impl Cartridge {
  pub fn new(config: config::Cartridge) -> Cartridge {
    let mbc = Mbc::from_config(&config);
    let ram_size = match mbc {
      Mbc::Mbc2 { .. } => 512,
      _ => config.ram_size.as_usize(),
    };
    Cartridge {
      mbc,
      rom: config.data,
      rom_offsets: (0x0000, 0x4000),
      ram: vec![0; ram_size].into_boxed_slice(),
      ram_offset: 0x0000,
    }
  }

  pub fn read_0000_3fff(&self, addr: u16) -> u8 {
    let (rom_lower, _) = self.rom_offsets;
    self.rom[(rom_lower | (addr as usize & 0x3fff)) & (self.rom.len() - 1)]
  }
  pub fn read_4000_7fff(&self, addr: u16) -> u8 {
    let (_, rom_upper) = self.rom_offsets;
    self.rom[(rom_upper | (addr as usize & 0x3fff)) & (self.rom.len() - 1)]
  }
  pub fn write_control(&mut self, reladdr: u16, value: u8) {
    match self.mbc {
      Mbc::None => (),
      Mbc::Mbc1 {
        ref mut state,
        multicart,
      } => match reladdr >> 8 {
        0x00..=0x1f => {
          state.ramg = (value & 0b1111) == 0b1010;
        }
        0x20..=0x3f => {
          state.bank1 = if value & 0b1_1111 == 0b0_0000 {
            0b0_0001
          } else {
            value & 0b1_1111
          };
          self.rom_offsets = state.rom_offsets(multicart);
        }
        0x40..=0x5f => {
          state.bank2 = value & 0b11;
          self.rom_offsets = state.rom_offsets(multicart);
          self.ram_offset = state.ram_offset();
        }
        0x60..=0x7f => {
          state.mode = (value & 0b1) == 0b1;
          self.rom_offsets = state.rom_offsets(multicart);
          self.ram_offset = state.ram_offset();
        }
        _ => (),
      },
      Mbc::Mbc2 { ref mut state } => match reladdr >> 8 {
        0x00..=0x3f if !reladdr.bit_bool(8) => {
          state.ramg = (value & 0x0f) == 0x0a;
        }
        0x00..=0x3f if reladdr.bit_bool(8) => {
          state.rom_bank = if value & 0b1111 == 0b0000 {
            0b0001
          } else {
            value & 0b1111
          };
          self.rom_offsets = (0x0000, ROM_BANK_SIZE * state.rom_bank as usize);
        }
        _ => (),
      },
      Mbc::Mbc3 {
        ref mut state,
        mbc30,
      } => match reladdr >> 8 {
        0x00..=0x1f => {
          state.map_en = (value & 0x0f) == 0x0a;
        }
        0x20..=0x3f => {
          state.rom_bank = if value == 0 { 1 } else { value };
          self.rom_offsets = (0x0000, ROM_BANK_SIZE * state.rom_bank as usize);
        }
        0x40..=0x5f => {
          state.map_select = value & 0b1111;
          if mbc30 {
            self.ram_offset = RAM_BANK_SIZE * (state.map_select & 0b111) as usize;
          } else {
            self.ram_offset = RAM_BANK_SIZE * (state.map_select & 0b011) as usize;
          }
        }
        _ => (),
      },
      Mbc::Mbc5 { ref mut state } => match reladdr >> 8 {
        0x00..=0x1f => {
          state.ramg = value == 0x0a;
        }
        0x20..=0x2f => {
          state.romb0 = value;
          self.rom_offsets = state.rom_offsets();
        }
        0x30..=0x3f => {
          state.romb1 = value & 0b1;
          self.rom_offsets = state.rom_offsets();
        }
        0x40..=0x5f => {
          state.ramb = value & 0b1111;
          self.ram_offset = RAM_BANK_SIZE * state.ramb as usize;
        }
        _ => (),
      },
      Mbc::Huc1 { ref mut state } => match reladdr >> 8 {
        0x00..=0x1f => {
          state.mode = value & 0xf;
        }
        0x20..=0x3f => {
          state.rom_bank = value & 0b11_1111;
          self.rom_offsets = (0x0000, ROM_BANK_SIZE * state.rom_bank as usize);
        }
        0x40..=0x5f => {
          state.ram_bank = value & 0b11;
          self.ram_offset = RAM_BANK_SIZE * state.ram_bank as usize;
        }
        _ => (),
      },
    }
  }
  pub fn read_a000_bfff(&self, addr: u16, default_value: u8) -> u8 {
    match self.mbc {
      Mbc::Mbc1 { ref state, .. } if state.ramg => self.read_ram(addr, default_value),
      Mbc::Mbc2 { ref state } if state.ramg => {
        (default_value & 0xf0) | (self.read_ram(addr, default_value) & 0x0f)
      }
      Mbc::Mbc3 { ref state, mbc30 } if state.map_en => match state.map_select {
        0x00..=0x03 => self.read_ram(addr, default_value),
        0x04..=0x07 if mbc30 => self.read_ram(addr, default_value),
        _ => default_value,
      },
      Mbc::Mbc5 { ref state } if state.ramg => self.read_ram(addr, default_value),
      Mbc::Huc1 { ref state } if state.mode == 0x00 || state.mode == 0x0a => {
        self.read_ram(addr, default_value)
      }
      _ => default_value,
    }
  }
  pub fn write_a000_bfff(&mut self, addr: u16, value: u8) {
    match self.mbc {
      Mbc::Mbc1 { ref state, .. } if state.ramg => self.write_ram(addr, value),
      Mbc::Mbc2 { ref state } if state.ramg => self.write_ram(addr, value & 0xf),
      Mbc::Mbc3 { ref state, mbc30 } if state.map_en => match state.map_select {
        0x00..=0x03 => self.write_ram(addr, value),
        0x04..=0x07 if mbc30 => self.write_ram(addr, value),
        _ => (),
      },
      Mbc::Mbc5 { ref state } if state.ramg => self.write_ram(addr, value),
      Mbc::Huc1 { ref state } if state.mode == 0x0a => self.write_ram(addr, value),
      _ => (),
    }
  }
  fn ram_addr(&self, addr: u16) -> usize {
    (self.ram_offset | (addr as usize & 0x1fff)) & (self.ram.len() - 1)
  }
  fn read_ram(&self, addr: u16, default_value: u8) -> u8 {
    if !self.ram.is_empty() {
      let addr = self.ram_addr(addr);
      self.ram[addr]
    } else {
      default_value
    }
  }
  fn write_ram(&mut self, addr: u16, value: u8) {
    if !self.ram.is_empty() {
      let addr = self.ram_addr(addr);
      self.ram[addr] = value;
    }
  }
}
