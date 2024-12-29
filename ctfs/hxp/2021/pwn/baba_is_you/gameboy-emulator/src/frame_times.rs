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
use std::time::{Duration, Instant};

pub struct FrameTimes {
    frame_duration: Duration,
    target_render_time: Instant,
}

impl FrameTimes {
    pub fn new(frame_duration: Duration) -> FrameTimes {
        let now = Instant::now();
        FrameTimes {
            frame_duration,
            target_render_time: now + frame_duration,
        }
    }

    pub fn update(&mut self, time_scale: f64) -> Duration {
        let delta = self.frame_duration;
        self.target_render_time += self.frame_duration.div_f64(time_scale);
        delta
    }

    pub fn target_render_time(&self) -> Instant {
        self.target_render_time
    }
}
