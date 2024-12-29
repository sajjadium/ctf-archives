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
use crate::cpu::register_file::Flags;
use crate::cpu::test::run_test;

#[test]
fn test_e0() {
  let machine = run_test(
    &[0xe0, 0x80], // LDH (n), A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.hardware.memory[0xff80], 0x42);
}

#[test]
fn test_e2() {
  let machine = run_test(
    &[0xe2], // LD (C), A
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.c = 0x80;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0xff80], 0x42);
}

#[test]
fn test_ea() {
  let machine = run_test(
    &[0xea, 0x04, 0x00, 0xed, 0x00], // LD (nn), A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 16);
  assert_eq!(machine.hardware.memory[0x04], 0x42);
}

#[test]
fn test_ee() {
  let machine = run_test(
    &[0xee, 0x38], // XOR (n)
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x7a);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_ee_zero() {
  let machine = run_test(
    &[0xee, 0x42], // XOR (n)
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}
