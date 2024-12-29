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
use crate::cpu::test::run_test;

#[test]
fn test_50() {
  let machine = run_test(
    &[0x50], // LD D, B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_51() {
  let machine = run_test(
    &[0x51], // LD D, C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_52() {
  let machine = run_test(
    &[0x52], // LD D, D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_53() {
  let machine = run_test(
    &[0x53], // LD D, E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_54() {
  let machine = run_test(
    &[0x54], // LD D, H
    |machine| {
      machine.cpu.regs.h = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_55() {
  let machine = run_test(
    &[0x55], // LD D, L
    |machine| {
      machine.cpu.regs.l = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_56() {
  let machine = run_test(
    &[0x56, 0xed, 0x42], // LD D, (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_57() {
  let machine = run_test(
    &[0x57], // LD D, A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_58() {
  let machine = run_test(
    &[0x58], // LD E, B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x42);
}

#[test]
fn test_59() {
  let machine = run_test(
    &[0x59], // LD E, C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x42);
}

#[test]
fn test_5a() {
  let machine = run_test(
    &[0x5a], // LD E, D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x42);
}

#[test]
fn test_5b() {
  let machine = run_test(
    &[0x5b], // LD E, E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x42);
}

#[test]
fn test_5c() {
  let machine = run_test(
    &[0x5c], // LD E, H
    |machine| {
      machine.cpu.regs.h = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x42);
}

#[test]
fn test_5d() {
  let machine = run_test(
    &[0x5d], // LD E, L
    |machine| {
      machine.cpu.regs.l = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x42);
}

#[test]
fn test_5e() {
  let machine = run_test(
    &[0x5e, 0xed, 0x42], // LD E, (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.e, 0x42);
}

#[test]
fn test_5f() {
  let machine = run_test(
    &[0x5f], // LD E, A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x42);
}
