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

#![allow(warnings)]
#![allow(clippy::all)]

pub mod config;
mod cpu;
pub mod emulation;
pub mod gameboy;
pub mod hardware;
pub mod machine;
mod util;

#[derive(Debug)]
pub enum GbKey {
  Right,
  Left,
  Up,
  Down,
  A,
  B,
  Select,
  Start,
}

use crate::emulation::EmuEvents;
pub use crate::gameboy::*;

pub trait Callbacks {
  fn debug_opcode(&mut self);
  fn bootrom_disabled(&mut self);
  fn trigger_emu_events(&mut self, emu_events: EmuEvents);
}

pub trait CoreContext {
  fn callbacks(&mut self) -> Option<&mut dyn Callbacks>;
}
