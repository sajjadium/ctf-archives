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
use crc::crc32;
use directories_next::ProjectDirs;
use log::{debug, info, warn};
use snafu::Snafu;
use std::fs::{self, File};
use std::io::{self, Read, Write};
use std::path::{Path, PathBuf};
use std::sync::Arc;

use crate::config::{Model, DEFAULT_MODEL_PRIORITY};
use crate::hardware::BootromData;

#[derive(Debug, Snafu)]
pub enum BootromError {
  #[snafu(display("IO error: {}", source))]
  Io { source: io::Error },
  #[snafu(display("Unrecognized boot ROM checksum: 0x{:08x}", crc32))]
  Checksum { crc32: u32 },
}

impl From<io::Error> for BootromError {
  fn from(source: io::Error) -> BootromError {
    BootromError::Io { source }
  }
}

pub struct Bootrom {
  pub model: Model,
  pub data: Arc<BootromData>,
}

fn bootroms_dir() -> Option<PathBuf> {
  ProjectDirs::from("", "Gekkio", "mooneye-gb").map(|dirs| dirs.data_dir().join("bootroms"))
}

impl Bootrom {
  pub fn from_path(path: &Path) -> Result<Bootrom, BootromError> {
    let mut file = File::open(path)?;
    let mut data = Box::new(BootromData::new());
    file.read_exact(&mut data.0)?;
    Bootrom::from_data(data.into())
  }
  pub fn from_data(data: Arc<BootromData>) -> Result<Bootrom, BootromError> {
    let checksum = crc32::checksum_ieee(&data.0);
    let model = match checksum {
      0xc2f5_cc97 => Some(Model::Dmg0),
      0x59c8_598e => Some(Model::Dmg),
      0xe692_0754 => Some(Model::Mgb),
      0xec8a_83b9 => Some(Model::Sgb),
      0x53d0_dd63 => Some(Model::Sgb2),
      _ => None,
    };
    match model {
      Some(model) => Ok(Bootrom { model, data }),
      None => Err(BootromError::Checksum { crc32: checksum }),
    }
  }
  #[cfg(not(feature = "include-bootroms"))]
  pub fn lookup(models: &[Model]) -> Option<Bootrom> {
    use std::env;

    let mut candidates = vec![];
    let models = if models.is_empty() {
      &DEFAULT_MODEL_PRIORITY
    } else {
      models
    };

    if let Some(dir) = bootroms_dir() {
      for model in models {
        candidates.push(dir.join(model.bootrom_file_name()));
      }
    }

    if let Ok(cwd) = env::current_dir() {
      for model in models {
        candidates.push(cwd.join(model.bootrom_file_name()));
      }
    }

    for path in candidates {
      let path_str = path.to_string_lossy();
      debug!("Scanning {} for a boot ROM", path_str);
      match Bootrom::from_path(&path) {
        Err(BootromError::Io { ref source }) if source.kind() == io::ErrorKind::NotFound => (),
        Err(ref e) => warn!("Warning: Boot rom \"{}\" ({})", path_str, e),
        Ok(bootrom) => {
          info!("Using {} boot ROM from {}", bootrom.model, path_str);
          return Some(bootrom);
        }
      }
    }
    None
  }
  #[cfg(feature = "include-bootroms")]
  pub fn lookup(models: &[Model]) -> Option<Bootrom> {
    let models = if models.is_empty() {
      &DEFAULT_MODEL_PRIORITY
    } else {
      models
    };
    models.first().map(|&model| {
      info!("Using included {} boot ROM", model);
      Bootrom {
        model,
        data: Arc::new(BootromData(
          match model {
            Model::Dmg0 => include_bytes!("../../bootroms/dmg0_boot.bin"),
            Model::Dmg => include_bytes!("../../bootroms/dmg_boot.bin"),
            Model::Mgb => include_bytes!("../../bootroms/mgb_boot.bin"),
            Model::Sgb => include_bytes!("../../bootroms/sgb_boot.bin"),
            Model::Sgb2 => include_bytes!("../../bootroms/sgb2_boot.bin"),
          }
          .clone(),
        )),
      }
    })
  }
  pub fn save_to_data_dir(&self) -> io::Result<()> {
    if let Some(dir) = bootroms_dir() {
      fs::create_dir_all(&dir)?;
      let path = dir.join(self.model.bootrom_file_name());
      let mut file = File::create(&path)?;
      file.write_all(&self.data.0)?;
      info!(
        "Saved {} boot ROM to {}",
        self.model,
        path.to_string_lossy()
      );
    }
    Ok(())
  }
}
