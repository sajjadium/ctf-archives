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
enum Time {
  None = 0,
  Div1 = 1,
  Div2 = 2,
  Div3 = 3,
  Div4 = 4,
  Div5 = 5,
  Div6 = 6,
  Div7 = 7,
}

impl Time {
  pub fn from_u8(value: u8) -> Option<Time> {
    use self::Time::*;
    match value {
      0 => Some(None),
      1 => Some(Div1),
      2 => Some(Div2),
      3 => Some(Div3),
      4 => Some(Div4),
      5 => Some(Div5),
      6 => Some(Div6),
      7 => Some(Div7),
      _ => Option::None,
    }
  }
}

#[derive(Clone)]
pub struct Sweep {
  time: Time,
  increasing: bool,
  shift: u8,
}

impl Sweep {
  pub fn new() -> Sweep {
    Sweep {
      time: Time::None,
      increasing: false,
      shift: 0,
    }
  }
  pub fn read_reg(&self) -> u8 {
    const MASK: u8 = 0x80;

    MASK | ((self.time as u8) << 4) | if self.increasing { 1 << 3 } else { 0 } | (self.shift)
  }
  pub fn write_reg(&mut self, value: u8) {
    self.time = Time::from_u8((value >> 4) & 0x07).unwrap();
    self.increasing = value & (1 << 3) != 0;
    self.shift = value & 0x07;
  }
}
