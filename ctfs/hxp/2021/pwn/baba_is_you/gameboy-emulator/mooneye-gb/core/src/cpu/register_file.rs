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
use std::fmt;

bitflags!(
  pub struct Flags: u8 {
    const ZERO         = 0b_1000_0000;
    const ADD_SUBTRACT = 0b_0100_0000;
    const HALF_CARRY   = 0b_0010_0000;
    const CARRY        = 0b_0001_0000;
  }
);

#[derive(Clone, Copy, Debug)]
pub enum Reg8 {
  A,
  B,
  C,
  D,
  E,
  H,
  L,
}

#[derive(Clone, Copy, Debug)]
pub enum Reg16 {
  AF,
  BC,
  DE,
  HL,
  SP,
}

#[derive(Clone, Copy, Debug)]
pub struct RegisterFile {
  pub pc: u16,
  pub sp: u16,
  pub a: u8,
  pub f: Flags,
  pub b: u8,
  pub c: u8,
  pub d: u8,
  pub e: u8,
  pub h: u8,
  pub l: u8,
}

impl RegisterFile {
  pub fn new() -> RegisterFile {
    RegisterFile {
      pc: 0,
      sp: 0,
      a: 0,
      f: Flags::empty(),
      b: 0,
      c: 0,
      d: 0,
      e: 0,
      h: 0,
      l: 0,
    }
  }

  pub fn read16(&self, reg: Reg16) -> u16 {
    use self::Reg16::*;
    match reg {
      AF => ((self.a as u16) << 8) | (self.f.bits() as u16),
      BC => ((self.b as u16) << 8) | (self.c as u16),
      DE => ((self.d as u16) << 8) | (self.e as u16),
      HL => ((self.h as u16) << 8) | (self.l as u16),
      SP => self.sp,
    }
  }

  pub fn write16(&mut self, reg: Reg16, value: u16) {
    use self::Reg16::*;
    match reg {
      AF => {
        self.a = (value >> 8) as u8;
        self.f = Flags::from_bits_truncate(value as u8)
      }
      BC => {
        self.b = (value >> 8) as u8;
        self.c = value as u8
      }
      DE => {
        self.d = (value >> 8) as u8;
        self.e = value as u8
      }
      HL => {
        self.h = (value >> 8) as u8;
        self.l = value as u8
      }
      SP => self.sp = value,
    }
  }

  #[inline]
  pub fn zf(&self) -> bool {
    self.f.contains(Flags::ZERO)
  }
  #[inline]
  pub fn nf(&self) -> bool {
    self.f.contains(Flags::ADD_SUBTRACT)
  }
  #[inline]
  pub fn hf(&self) -> bool {
    self.f.contains(Flags::HALF_CARRY)
  }
  #[inline]
  pub fn cf(&self) -> bool {
    self.f.contains(Flags::CARRY)
  }
  #[inline]
  pub fn set_zf(&mut self, zf: bool) {
    self.f.set(Flags::ZERO, zf);
  }
  #[inline]
  pub fn set_nf(&mut self, nf: bool) {
    self.f.set(Flags::ADD_SUBTRACT, nf);
  }
  #[inline]
  pub fn set_hf(&mut self, hf: bool) {
    self.f.set(Flags::HALF_CARRY, hf);
  }
  #[inline]
  pub fn set_cf(&mut self, cf: bool) {
    self.f.set(Flags::CARRY, cf);
  }
}

impl fmt::Display for RegisterFile {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    write!(
      f,
      "PC:{:04x} SP:{:04x} \
       A:{:02x} F:{:04b} B:{:02x} C:{:02x} \
       D:{:02x} E:{:02x} H:{:02x} L:{:02x}",
      self.pc, self.sp, self.a, self.f, self.b, self.c, self.d, self.e, self.h, self.l
    )
  }
}
