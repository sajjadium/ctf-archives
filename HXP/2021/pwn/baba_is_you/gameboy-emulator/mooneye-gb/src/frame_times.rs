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
use std::thread;
use std::time::{Duration, Instant};

pub struct FrameTimes {
  pub frame_duration: Duration,
  pub last_time: Instant,
  pub target_time: Instant,
}

impl FrameTimes {
  pub fn new(frame_duration: Duration) -> FrameTimes {
    let now = Instant::now();
    FrameTimes {
      frame_duration,
      last_time: now,
      target_time: now + frame_duration,
    }
  }
  pub fn update(&mut self) -> Duration {
    let now = Instant::now();
    let delta = now - self.last_time;
    self.last_time = now;
    self.target_time += self.frame_duration;
    delta
  }
  pub fn limit(&self) {
    let now = Instant::now();
    if now < self.target_time {
      thread::sleep(self.target_time - now);
    }
  }
}
