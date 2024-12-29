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
use serde_derive::Deserialize;
use std::fmt;
use std::str::FromStr;

pub static DEFAULT_MODEL_PRIORITY: [Model; 5] =
  [Model::Dmg, Model::Mgb, Model::Sgb2, Model::Sgb, Model::Dmg0];

#[derive(Copy, Clone, Debug, PartialEq, Eq, Deserialize)]
pub enum Model {
  Dmg0,
  Dmg,
  Mgb,
  Sgb,
  Sgb2,
}

#[derive(Debug)]
pub struct InvalidModel;

impl std::error::Error for InvalidModel {}
impl fmt::Display for InvalidModel {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    write!(f, "invalid model name")
  }
}

impl FromStr for Model {
  type Err = InvalidModel;

  fn from_str(s: &str) -> Result<Self, Self::Err> {
    match s {
      "dmg0" => Ok(Model::Dmg0),
      "dmg" => Ok(Model::Dmg),
      "mgb" => Ok(Model::Mgb),
      "sgb" => Ok(Model::Sgb),
      "sgb2" => Ok(Model::Sgb2),
      _ => Err(InvalidModel),
    }
  }
}

impl Model {
  pub fn bootrom_file_name(&self) -> &'static str {
    use self::Model::*;
    match *self {
      Dmg0 => "dmg0_boot.bin",
      Dmg => "dmg_boot.bin",
      Mgb => "mgb_boot.bin",
      Sgb => "sgb_boot.bin",
      Sgb2 => "sgb2_boot.bin",
    }
  }
}

impl fmt::Display for Model {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    use self::Model::*;
    f.write_str(match *self {
      Dmg0 => "DMG (Game Boy), early version",
      Dmg => "DMG (Game Boy)",
      Mgb => "MGB (Game Boy Pocket)",
      Sgb => "SGB (Super Game Boy)",
      Sgb2 => "SGB2 (Super Game Boy 2)",
    })
  }
}
