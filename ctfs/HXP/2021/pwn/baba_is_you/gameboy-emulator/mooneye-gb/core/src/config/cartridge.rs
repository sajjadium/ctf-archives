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
use snafu::Snafu;
use std::fmt;
use std::fs::File;
use std::io::{self, Read};
use std::path::Path;
use std::str;
use std::sync::Arc;

use crate::gameboy::ROM_BANK_SIZE;

#[derive(Clone, Debug)]
pub struct Cartridge {
  pub data: Arc<[u8]>,
  pub title: String,
  pub cartridge_type: CartridgeType,
  pub rom_size: CartridgeRomSize,
  pub ram_size: CartridgeRamSize,
}

#[derive(Debug, Snafu)]
pub enum CartridgeError {
  #[snafu(display("IO error: {}", source))]
  Io { source: io::Error },
  #[snafu(display("Invalid cartridge: {}", msg))]
  Validation { msg: String },
}

impl From<io::Error> for CartridgeError {
  fn from(source: io::Error) -> CartridgeError {
    CartridgeError::Io { source }
  }
}

impl Cartridge {
  pub fn no_cartridge() -> Cartridge {
    Cartridge {
      data: vec![0xff; 2].into_boxed_slice().into(),
      title: "-".to_string(),
      cartridge_type: CartridgeType::NoMbc {
        ram: false,
        battery: false,
      },
      rom_size: CartridgeRomSize::NoRomBanks,
      ram_size: CartridgeRamSize::NoRam,
    }
  }
  pub fn from_path(path: &Path) -> Result<Cartridge, CartridgeError> {
    let mut file = File::open(path)?;
    let mut data = vec![];
    file.read_to_end(&mut data)?;
    Cartridge::from_data(data.into())
  }
  pub fn from_data(data: Arc<[u8]>) -> Result<Cartridge, CartridgeError> {
    if data.len() < 0x8000 || data.len() % 0x4000 != 0 {
      return Err(CartridgeError::Validation {
        msg: format!("Invalid length: {} bytes", data.len()),
      });
    }
    let new_cartridge = data[0x14b] == 0x33;

    let title = {
      let slice = if new_cartridge {
        &data[0x134..0x13f]
      } else {
        &data[0x134..0x143]
      };
      let utf8 = str::from_utf8(slice).map_err(|_| CartridgeError::Validation {
        msg: "Invalid ROM title".to_string(),
      })?;

      utf8.trim_end_matches('\0').to_string()
    };

    let mut cartridge_type =
      CartridgeType::from_u8(data[0x147]).ok_or_else(|| CartridgeError::Validation {
        msg: format!("Unsupported cartridge type {:02x}", data[0x147]),
      })?;
    if let CartridgeType::Mbc1 { multicart, .. } = &mut cartridge_type {
      *multicart = is_mbc1_multicart(&data);
    }
    let rom_size =
      CartridgeRomSize::from_u8(data[0x148]).ok_or_else(|| CartridgeError::Validation {
        msg: format!("Unsupported rom size {:02x}", data[0x148]),
      })?;
    let ram_size =
      CartridgeRamSize::from_u8(data[0x149]).ok_or_else(|| CartridgeError::Validation {
        msg: format!("Unsupported ram size {:02x}", data[0x149]),
      })?;

    if cartridge_type.has_ram_chip() && ram_size == CartridgeRamSize::NoRam {
      return Err(CartridgeError::Validation {
        msg: format!("{:?} cartridge without ram", cartridge_type),
      });
    }
    if !cartridge_type.has_ram_chip() && ram_size != CartridgeRamSize::NoRam {
      return Err(CartridgeError::Validation {
        msg: format!(
          "{:?} cartridge with ram size {:02x}",
          cartridge_type, data[0x149]
        ),
      });
    }
    if data.len() != rom_size.as_usize() {
      return Err(CartridgeError::Validation {
        msg: format!(
          "Expected {} bytes of cartridge ROM, got {:?}",
          rom_size.as_usize(),
          data.len()
        ),
      });
    }

    Ok(Cartridge {
      data,
      title,
      cartridge_type,
      rom_size,
      ram_size,
    })
  }
}

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum CartridgeType {
  NoMbc {
    ram: bool,
    battery: bool,
  },
  Mbc1 {
    ram: bool,
    battery: bool,
    multicart: bool,
  },
  Mbc2 {
    battery: bool,
  },
  Mbc3 {
    ram: bool,
    battery: bool,
    rtc: bool,
  },
  Mbc5 {
    ram: bool,
    battery: bool,
    rumble: bool,
  },
  Mbc6,
  Mbc7,
  Huc1,
  Huc3,
}

impl CartridgeType {
  fn from_u8(value: u8) -> Option<CartridgeType> {
    use self::CartridgeType::*;
    match value {
      0x00 => Some(NoMbc {
        ram: false,
        battery: false,
      }),
      0x08 => Some(NoMbc {
        ram: true,
        battery: false,
      }),
      0x09 => Some(NoMbc {
        ram: true,
        battery: true,
      }),
      0x01 => Some(Mbc1 {
        ram: false,
        battery: false,
        multicart: false,
      }),
      0x02 => Some(Mbc1 {
        ram: true,
        battery: false,
        multicart: false,
      }),
      0x03 => Some(Mbc1 {
        ram: true,
        battery: true,
        multicart: false,
      }),
      0x05 => Some(Mbc2 { battery: false }),
      0x06 => Some(Mbc2 { battery: true }),
      0x11 => Some(Mbc3 {
        ram: false,
        battery: false,
        rtc: false,
      }),
      0x12 => Some(Mbc3 {
        ram: true,
        battery: false,
        rtc: false,
      }),
      0x13 => Some(Mbc3 {
        ram: true,
        battery: true,
        rtc: false,
      }),
      0x0f => Some(Mbc3 {
        ram: false,
        battery: true,
        rtc: true,
      }),
      0x10 => Some(Mbc3 {
        ram: true,
        battery: true,
        rtc: true,
      }),
      0x19 => Some(Mbc5 {
        ram: false,
        battery: false,
        rumble: false,
      }),
      0x1a => Some(Mbc5 {
        ram: true,
        battery: false,
        rumble: false,
      }),
      0x1b => Some(Mbc5 {
        ram: true,
        battery: true,
        rumble: false,
      }),
      0x1c => Some(Mbc5 {
        ram: false,
        battery: false,
        rumble: true,
      }),
      0x1d => Some(Mbc5 {
        ram: true,
        battery: false,
        rumble: true,
      }),
      0x1e => Some(Mbc5 {
        ram: true,
        battery: true,
        rumble: true,
      }),
      0x20 => Some(Mbc6),
      0x22 => Some(Mbc7),
      0xff => Some(Huc1),
      0xfe => Some(Huc3),
      _ => None,
    }
  }
  fn has_ram_chip(&self) -> bool {
    use self::CartridgeType::*;
    match *self {
      NoMbc { ram, .. } => ram,
      Mbc1 { ram, .. } => ram,
      Mbc2 { .. } => false, // MBC2 has internal RAM and doesn't use a RAM chip
      Mbc3 { ram, .. } => ram,
      Mbc5 { ram, .. } => ram,
      Mbc6 | Mbc7 | Huc1 | Huc3 => true,
    }
  }
}

#[derive(Copy, Clone, PartialEq, Eq)]
pub enum CartridgeRomSize {
  NoRomBanks = 0x00,
  RomBanks4 = 0x01,
  RomBanks8 = 0x02,
  RomBanks16 = 0x03,
  RomBanks32 = 0x04,
  RomBanks64 = 0x05,
  RomBanks128 = 0x06,
  RomBanks256 = 0x07,
  RomBanks512 = 0x08,
}

impl fmt::Debug for CartridgeRomSize {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    use self::CartridgeRomSize::*;
    write!(
      f,
      "{}",
      match *self {
        NoRomBanks => "256 kbit",
        RomBanks4 => "512 kbit",
        RomBanks8 => "1 Mbit",
        RomBanks16 => "2 Mbit",
        RomBanks32 => "4 Mbit",
        RomBanks64 => "8 Mbit",
        RomBanks128 => "16 Mbit",
        RomBanks256 => "32 Mbit",
        RomBanks512 => "64 Mbit",
      }
    )
  }
}

impl CartridgeRomSize {
  fn from_u8(value: u8) -> Option<CartridgeRomSize> {
    use self::CartridgeRomSize::*;
    match value {
      0x00 => Some(NoRomBanks),
      0x01 => Some(RomBanks4),
      0x02 => Some(RomBanks8),
      0x03 => Some(RomBanks16),
      0x04 => Some(RomBanks32),
      0x05 => Some(RomBanks64),
      0x06 => Some(RomBanks128),
      0x07 => Some(RomBanks256),
      0x08 => Some(RomBanks512),
      _ => None,
    }
  }
  pub fn banks(&self) -> usize {
    use self::CartridgeRomSize::*;
    match *self {
      NoRomBanks => 2,
      RomBanks4 => 4,
      RomBanks8 => 8,
      RomBanks16 => 16,
      RomBanks32 => 32,
      RomBanks64 => 64,
      RomBanks128 => 128,
      RomBanks256 => 256,
      RomBanks512 => 512,
    }
  }
  pub fn as_usize(&self) -> usize {
    self.banks() * ROM_BANK_SIZE
  }
}

#[derive(Copy, Clone, PartialEq, Eq)]
pub enum CartridgeRamSize {
  NoRam = 0x00,
  Ram2K = 0x01,
  Ram8K = 0x02,
  Ram32K = 0x03,
  Ram128K = 0x04,
  Ram64K = 0x05,
}

impl fmt::Debug for CartridgeRamSize {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    use self::CartridgeRamSize::*;
    write!(
      f,
      "{}",
      match *self {
        NoRam => "-",
        Ram2K => "16 kbit",
        Ram8K => "64 kbit",
        Ram32K => "256 kbit",
        Ram128K => "1 Mbit",
        Ram64K => "512 kbit",
      }
    )
  }
}

impl CartridgeRamSize {
  fn from_u8(value: u8) -> Option<CartridgeRamSize> {
    use self::CartridgeRamSize::*;
    match value {
      0x00 => Some(NoRam),
      0x01 => Some(Ram2K),
      0x02 => Some(Ram8K),
      0x03 => Some(Ram32K),
      0x04 => Some(Ram128K),
      0x05 => Some(Ram64K),
      _ => None,
    }
  }
  pub fn as_usize(&self) -> usize {
    use self::CartridgeRamSize::*;
    match *self {
      NoRam => 0,
      Ram2K => 2048,
      Ram8K => 8192,
      Ram32K => 32768,
      Ram128K => 131_072,
      Ram64K => 65536,
    }
  }
}

fn is_mbc1_multicart(rom: &[u8]) -> bool {
  // Only 8 Mbit MBC1 multicarts exist. Since it's not clear how other ROM sizes would be wired,
  // it's pointless to try to support them
  if rom.len() != 1_048_576 {
    return false;
  }

  let nintendo_logo_count = (0..4)
    .map(|page| {
      let start = page * 0x40000 + 0x0104;
      let end = start + 0x30;

      crc32::checksum_ieee(&rom[start..end])
    })
    .filter(|&checksum| checksum == 0x4619_5417)
    .count();

  // A multicart should have at least two games + a menu with valid logo data
  nintendo_logo_count >= 3
}
