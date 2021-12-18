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
use std::sync::Arc;

mod bootrom;
mod cartridge;
mod model;

pub use self::bootrom::Bootrom;
pub use self::cartridge::{Cartridge, CartridgeRamSize, CartridgeRomSize, CartridgeType};
pub use self::model::{Model, DEFAULT_MODEL_PRIORITY};
use crate::hardware::BootromData;

#[derive(Clone)]
pub struct HardwareConfig {
  pub model: Model,
  pub bootrom: Option<Arc<BootromData>>,
  pub cartridge: Cartridge,
}
