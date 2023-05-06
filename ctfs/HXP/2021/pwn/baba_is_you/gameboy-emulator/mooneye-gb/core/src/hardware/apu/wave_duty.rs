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
pub enum WaveDuty {
  HalfQuarter = 0,
  Quarter = 1,
  Half = 2,
  ThreeQuarters = 3,
}

impl WaveDuty {
  pub fn from_u8(value: u8) -> Option<WaveDuty> {
    use self::WaveDuty::*;
    match value {
      0 => Some(HalfQuarter),
      1 => Some(Quarter),
      2 => Some(Half),
      3 => Some(ThreeQuarters),
      _ => None,
    }
  }
}
