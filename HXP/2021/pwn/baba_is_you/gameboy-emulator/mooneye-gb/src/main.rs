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
#![windows_subsystem = "windows"]

use anyhow::Error;
use log::{error, info, warn};
use mooneye_gb::config::{Bootrom, Cartridge, Model};
use simplelog::{LevelFilter, TermLogger, TerminalMode};
use std::ffi::OsStr;
use std::path::{Path, PathBuf};
use std::process;

mod fps_counter;
mod frame_times;
mod frontend;
mod perf_counter;

const VERSION: &str = env!("CARGO_PKG_VERSION");

const USAGE: &str = concat!(
  "Mooneye GB v",
  env!("CARGO_PKG_VERSION"),
  "

Usage:
  mooneye-gb [options] [<rom>]
  mooneye-gb (-h | --help)

Options:
  -h, --help               Help
  -m MODEL, --model MODEL  Emulate a specific Game Boy model.
                           Valid values: dmg0, dmg, mgb, sgb, sgb2.
  -b FILE, --bootrom FILE  Use a boot ROM
"
);

#[derive(Debug)]
struct Args {
  help: bool,
  flag_model: Option<Model>,
  flag_bootrom: Option<PathBuf>,
  arg_rom: Option<PathBuf>,
}

fn parse_path(s: &OsStr) -> Result<PathBuf, &'static str> {
  Ok(s.into())
}

fn parse_args(mut args: pico_args::Arguments) -> Result<Args, Error> {
  let help = args.contains(["-h", "--help"]);
  let flag_model = args.opt_value_from_str(["-m", "--model"])?;
  let flag_bootrom = args.opt_value_from_os_str(["-b", "--bootrom"], parse_path)?;
  let arg_rom = args.opt_free_from_os_str(parse_path)?;
  let _ = args.finish();
  Ok(Args {
    help,
    flag_model,
    flag_bootrom,
    arg_rom,
  })
}

fn main() -> Result<(), Error> {
  match parse_args(pico_args::Arguments::from_env()) {
    Err(e) => {
      eprintln!("{}", e);
      eprintln!("{}", USAGE);
      process::exit(1);
    }
    Ok(Args { help: true, .. }) => {
      eprintln!("{}", USAGE);
      process::exit(1);
    }
    Ok(args) => run(args),
  }
}

fn read_boot_rom(path: &Path, expected_model: Option<Model>) -> Bootrom {
  let bootrom = Bootrom::from_path(path).unwrap_or_else(|err| {
    error!(
      "Failed to read boot rom from \"{}\" ({})",
      path.display(),
      err
    );
    process::exit(1)
  });
  if let Some(model) = expected_model {
    if model != bootrom.model {
      warn!("Warning: boot ROM is not for {}", model);
    }
  }
  bootrom
}

fn run(args: Args) -> Result<(), Error> {
  let _ = TermLogger::init(
    LevelFilter::Debug,
    simplelog::Config::default(),
    TerminalMode::Mixed,
  );
  info!("Starting Mooneye GB v{}", VERSION);

  let bootrom = match (args.flag_model, args.flag_bootrom) {
    (_, Some(path)) => Some(read_boot_rom(&path, args.flag_model)),
    (Some(model), None) => {
      let result = Bootrom::lookup(&[model]);
      if result.is_none() {
        error!("Could not find a boot rom for {}", model);
        process::exit(1)
      }
      result
    }
    (None, None) => Bootrom::lookup(&[]),
  };

  let cartridge = args.arg_rom.map(|path| {
    Cartridge::from_path(&path).unwrap_or_else(|err| {
      error!("Failed to read rom from \"{}\" ({})", path.display(), err);
      process::exit(1)
    })
  });

  frontend::run(bootrom, cartridge)?;

  Ok(())
}
