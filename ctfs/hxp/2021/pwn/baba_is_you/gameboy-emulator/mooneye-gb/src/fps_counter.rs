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

const HISTORY_SIZE: usize = 64;

pub struct FpsCounter {
  history: ArrayDeque<[f64; HISTORY_SIZE], Wrapping>,
}

impl FpsCounter {
  pub fn new() -> FpsCounter {
    FpsCounter {
      history: ArrayDeque::new(),
    }
  }
  pub fn update(&mut self, delta_s: f64) {
    let _ = self.history.push_back(delta_s);
  }
  pub fn get_fps(&self) -> f64 {
    let sum = self.history.iter().sum::<f64>();
    if sum == 0.0 {
      0.0
    } else {
      self.history.len() as f64 / sum
    }
  }
}
