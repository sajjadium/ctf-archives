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
use crate::cpu::{Cpu, CpuContext, Step};
use crate::hardware::interrupts::InterruptLine;
use crate::{Callbacks, CoreContext};

mod cb_test;
mod test_0x;
mod test_1x;
mod test_2x;
mod test_3x;
mod test_4x;
mod test_5x;
mod test_6x;
mod test_7x;
mod test_ax;
mod test_cx;
mod test_ex;
mod test_fx;

mod test_add16;
mod test_add16_sp_e;
mod test_dec16;
mod test_inc16;
mod test_load16;
mod test_load16_hl_sp_e;
mod test_load16_sp_hl;
mod test_pop16;
mod test_push16;

pub struct TestMachine {
  cpu: Cpu,
  hardware: TestHardware,
  step: Step,
}

pub struct TestHardware {
  memory: Vec<u8>,
  t_cycles: usize,
}

impl TestHardware {
  fn from_memory(input: &[u8]) -> TestHardware {
    let mut memory = vec![0x00; 0x10000];
    memory[0..input.len()].copy_from_slice(input);
    TestHardware {
      memory,
      t_cycles: 0,
    }
  }
  fn clock_cycles(&self) -> usize {
    self.t_cycles
  }
  fn read(&self, addr: u16) -> u8 {
    self.memory[addr as usize]
  }
}

impl CoreContext for TestHardware {
  fn callbacks(&mut self) -> Option<&mut dyn Callbacks> {
    None
  }
}

impl CpuContext for TestHardware {
  fn read_cycle(&mut self, addr: u16) -> u8 {
    self.t_cycles += 4;
    self.read(addr)
  }
  fn read_cycle_intr(&mut self, addr: u16) -> (InterruptLine, u8) {
    (InterruptLine::empty(), self.read_cycle(addr))
  }
  fn write_cycle(&mut self, addr: u16, value: u8) {
    self.t_cycles += 4;
    self.memory[addr as usize] = value;
  }
  fn write_cycle_intr(&mut self, addr: u16, value: u8) -> InterruptLine {
    self.write_cycle(addr, value);
    InterruptLine::empty()
  }
  fn tick_cycle(&mut self) {
    self.t_cycles += 4;
  }
  fn has_interrupt(&self) -> bool {
    false
  }
  fn ack_interrupt(&mut self, _: InterruptLine) {}
}

pub fn run_test<I: Fn(&mut TestMachine) -> ()>(instructions: &[u8], init: I) -> TestMachine {
  let mut memory = instructions.to_vec();
  memory.push(0xed);

  let mut machine = TestMachine {
    cpu: Cpu::new(),
    hardware: TestHardware::from_memory(&memory),
    step: Step::Running,
  };
  init(&mut machine);

  machine.step = machine
    .cpu
    .execute_step(&mut machine.hardware, machine.step);
  machine.hardware.t_cycles = 0;

  while machine.cpu.opcode != 0xed && machine.step != Step::Halt {
    machine.step = machine
      .cpu
      .execute_step(&mut machine.hardware, machine.step);
  }
  machine
}
