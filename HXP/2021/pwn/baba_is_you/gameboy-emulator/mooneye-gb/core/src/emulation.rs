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
use std::ops::{Add, AddAssign, Sub};

bitflags!(
  pub struct EmuEvents: u8 {
    const DEBUG_OP         = 0b_0000_0001;
    const VSYNC            = 0b_0000_0010;
    const BOOTROM_DISABLED = 0b_0000_0100;
  }
);

#[derive(Copy, Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct EmuTime {
  pub machine_cycles: u64,
}

impl EmuTime {
  pub fn zero() -> EmuTime {
    EmuTime { machine_cycles: 0 }
  }
  pub fn from_machine_cycles(machine_cycles: u64) -> EmuTime {
    EmuTime { machine_cycles }
  }
}

impl fmt::Display for EmuTime {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    write!(f, "{} machine cycles", self.machine_cycles)
  }
}

impl Add<EmuTime> for EmuTime {
  type Output = EmuTime;
  fn add(self, rhs: EmuTime) -> EmuTime {
    EmuTime {
      machine_cycles: self.machine_cycles + rhs.machine_cycles,
    }
  }
}

impl AddAssign<EmuTime> for EmuTime {
  fn add_assign(&mut self, rhs: EmuTime) {
    self.machine_cycles += rhs.machine_cycles;
  }
}

impl Sub<EmuTime> for EmuTime {
  type Output = EmuTime;
  fn sub(self, rhs: EmuTime) -> EmuTime {
    EmuTime {
      machine_cycles: self.machine_cycles - rhs.machine_cycles,
    }
  }
}
