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
fn test_40() {
  let machine = run_test(
    &[0x40], // LD B, B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_41() {
  let machine = run_test(
    &[0x41], // LD B, C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_42() {
  let machine = run_test(
    &[0x42], // LD B, D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_43() {
  let machine = run_test(
    &[0x43], // LD B, E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_44() {
  let machine = run_test(
    &[0x44], // LD B, H
    |machine| {
      machine.cpu.regs.h = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_45() {
  let machine = run_test(
    &[0x45], // LD B, L
    |machine| {
      machine.cpu.regs.l = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_46() {
  let machine = run_test(
    &[0x46, 0xed, 0x42], // LD B, (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_47() {
  let machine = run_test(
    &[0x47], // LD B, A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_48() {
  let machine = run_test(
    &[0x48], // LD C, B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x42);
}

#[test]
fn test_49() {
  let machine = run_test(
    &[0x49], // LD C, C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x42);
}

#[test]
fn test_4a() {
  let machine = run_test(
    &[0x4a], // LD C, D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x42);
}

#[test]
fn test_4b() {
  let machine = run_test(
    &[0x4b], // LD C, E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x42);
}

#[test]
fn test_4c() {
  let machine = run_test(
    &[0x4c], // LD C, H
    |machine| {
      machine.cpu.regs.h = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x42);
}

#[test]
fn test_4d() {
  let machine = run_test(
    &[0x4d], // LD C, L
    |machine| {
      machine.cpu.regs.l = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x42);
}

#[test]
fn test_4e() {
  let machine = run_test(
    &[0x4e, 0xed, 0x42], // LD C, (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.c, 0x42);
}

#[test]
fn test_4f() {
  let machine = run_test(
    &[0x4f], // LD C, A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x42);
}
