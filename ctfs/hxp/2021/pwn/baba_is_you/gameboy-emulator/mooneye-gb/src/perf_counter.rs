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
use arraydeque::behavior::Wrapping;
use arraydeque::ArrayDeque;

use mooneye_gb::emulation::EmuTime;

const HISTORY_SIZE: usize = 64;

/// A cycles-per-second counter
pub struct PerfCounter {
  history: ArrayDeque<[f64; HISTORY_SIZE], Wrapping>,
}

impl PerfCounter {
  pub fn new() -> PerfCounter {
    PerfCounter {
      history: ArrayDeque::new(),
    }
  }
  pub fn update(&mut self, duration: EmuTime, delta_s: f64) {
    let machine_cycles_per_s = duration.machine_cycles as f64 / delta_s;
    let _ = self.history.push_back(machine_cycles_per_s);
  }
  pub fn get_machine_cycles_per_s(&self) -> f64 {
    if self.history.is_empty() {
      0.0
    } else {
      self.history.iter().sum::<f64>() / self.history.len() as f64
    }
  }
}
