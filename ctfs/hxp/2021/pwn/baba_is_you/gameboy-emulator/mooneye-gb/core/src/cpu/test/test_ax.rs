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
fn test_a8() {
  let machine = run_test(
    &[0xa8], // XOR B
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.b = 0x38;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x7a);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_a8_zero() {
  let machine = run_test(
    &[0xa8], // XOR B
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}

#[test]
fn test_a9() {
  let machine = run_test(
    &[0xa9], // XOR C
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.c = 0x38;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x7a);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_a9_zero() {
  let machine = run_test(
    &[0xa9], // XOR C
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}

#[test]
fn test_aa() {
  let machine = run_test(
    &[0xaa], // XOR D
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.d = 0x38;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x7a);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_aa_zero() {
  let machine = run_test(
    &[0xaa], // XOR D
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}

#[test]
fn test_ab() {
  let machine = run_test(
    &[0xab], // XOR E
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.e = 0x38;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x7a);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_ab_zero() {
  let machine = run_test(
    &[0xab], // XOR E
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}

#[test]
fn test_ac() {
  let machine = run_test(
    &[0xac], // XOR H
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.h = 0x38;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x7a);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_ac_zero() {
  let machine = run_test(
    &[0xac], // XOR H
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.h = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}

#[test]
fn test_ad() {
  let machine = run_test(
    &[0xad], // XOR L
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.l = 0x38;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x7a);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_ad_zero() {
  let machine = run_test(
    &[0xad], // XOR L
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.l = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}

#[test]
fn test_ae() {
  let machine = run_test(
    &[0xae, 0xed, 0x38], // XOR (HL)
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x7a);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_ae_zero() {
  let machine = run_test(
    &[0xae, 0xed, 0x42], // XOR (HL)
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}

#[test]
fn test_af() {
  let machine = run_test(
    &[0xaf], // XOR A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO);
}
