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
use crate::config::HardwareConfig;
use crate::cpu::register_file::RegisterFile;
use crate::cpu::{Cpu, Step};
use crate::emulation::{EmuEvents, EmuTime};
use crate::gameboy;
use crate::hardware::Hardware;
use crate::GbKey;

#[derive(Clone)]
pub struct Machine {
  cpu: Cpu,
  hardware: Hardware,
  step: Step,
}

impl Machine {
  pub fn new(config: HardwareConfig) -> Machine {
    Machine {
      cpu: Cpu::new(),
      hardware: Hardware::new(config),
      step: Step::Running,
    }
  }
  pub fn emulate_step(&mut self) -> (EmuEvents, EmuTime) {
    let step = self.cpu.execute_step(&mut self.hardware, self.step);
    self.step = step;
    (self.hardware.ack_emu_events(), self.hardware.emu_time())
  }
  pub fn emulate(&mut self, target_time: EmuTime) -> (EmuEvents, EmuTime) {
    let mut step = self.step;
    loop {
      step = self.cpu.execute_step(&mut self.hardware, step);
      if !self.hardware.emu_events().is_empty() || self.hardware.emu_time() >= target_time {
        break;
      }
    }
    self.step = step;
    (self.hardware.ack_emu_events(), self.hardware.emu_time())
  }
  pub fn emu_time(&self) -> EmuTime {
    self.hardware.emu_time()
  }
  pub fn key_down(&mut self, key: GbKey) {
    self.hardware.key_down(key);
  }
  pub fn key_up(&mut self, key: GbKey) {
    self.hardware.key_up(key);
  }
  pub fn regs(&self) -> RegisterFile {
    self.cpu.regs
  }
  pub fn screen_buffer(&self) -> &gameboy::ScreenBuffer {
    self.hardware.screen_buffer()
  }
  pub fn hardware(&self) -> &Hardware {
    &self.hardware
  }
}
