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
fn test_60() {
  let machine = run_test(
    &[0x60], // LD H, B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.h, 0x42);
}

#[test]
fn test_61() {
  let machine = run_test(
    &[0x61], // LD H, C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.h, 0x42);
}

#[test]
fn test_62() {
  let machine = run_test(
    &[0x62], // LD H, D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.h, 0x42);
}

#[test]
fn test_63() {
  let machine = run_test(
    &[0x63], // LD H, E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.h, 0x42);
}

#[test]
fn test_64() {
  let machine = run_test(
    &[0x64], // LD H, H
    |machine| {
      machine.cpu.regs.h = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.h, 0x42);
}

#[test]
fn test_65() {
  let machine = run_test(
    &[0x65], // LD H, L
    |machine| {
      machine.cpu.regs.l = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.h, 0x42);
}

#[test]
fn test_66() {
  let machine = run_test(
    &[0x66, 0xed, 0x42], // LD H, (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.h, 0x42);
}

#[test]
fn test_67() {
  let machine = run_test(
    &[0x67], // LD H, A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.h, 0x42);
}

#[test]
fn test_68() {
  let machine = run_test(
    &[0x68], // LD L, B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.l, 0x42);
}

#[test]
fn test_69() {
  let machine = run_test(
    &[0x69], // LD L, C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.l, 0x42);
}

#[test]
fn test_6a() {
  let machine = run_test(
    &[0x6a], // LD L, D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.l, 0x42);
}

#[test]
fn test_6b() {
  let machine = run_test(
    &[0x6b], // LD L, E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.l, 0x42);
}

#[test]
fn test_6c() {
  let machine = run_test(
    &[0x6c], // LD L, H
    |machine| {
      machine.cpu.regs.h = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.l, 0x42);
}

#[test]
fn test_6d() {
  let machine = run_test(
    &[0x6d], // LD L, L
    |machine| {
      machine.cpu.regs.l = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.l, 0x42);
}

#[test]
fn test_6e() {
  let machine = run_test(
    &[0x6e, 0xed, 0x42], // LD L, (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.l, 0x42);
}

#[test]
fn test_6f() {
  let machine = run_test(
    &[0x6f], // LD L, A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.l, 0x42);
}
