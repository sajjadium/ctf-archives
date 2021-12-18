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
#[derive(Clone)]
pub struct Envelope {
  volume: u8,
  increasing: bool,
  length: u8,
}

impl Envelope {
  pub fn new() -> Envelope {
    Envelope {
      volume: 0,
      increasing: false,
      length: 0,
    }
  }
  pub fn read_reg(&self) -> u8 {
    (self.volume << 4) | if self.increasing { 1 << 3 } else { 0 } | self.length
  }
  pub fn write_reg(&mut self, value: u8) {
    self.volume = (value >> 4) & 0x0f;
    self.increasing = value & (1 << 3) != 0;
    self.length = value & 0x07;
  }
}
