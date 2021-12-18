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
use crate::cpu::Step;

#[test]
fn test_70() {
  let machine = run_test(
    &[0x70, 0xed, 0x00], // LD (HL), B
    |machine| {
      machine.cpu.regs.b = 0x42;
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x42);
}

#[test]
fn test_71() {
  let machine = run_test(
    &[0x71, 0xed, 0x00], // LD (HL), C
    |machine| {
      machine.cpu.regs.c = 0x42;
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x42);
}

#[test]
fn test_72() {
  let machine = run_test(
    &[0x72, 0xed, 0x00], // LD (HL), D
    |machine| {
      machine.cpu.regs.d = 0x42;
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x42);
}

#[test]
fn test_73() {
  let machine = run_test(
    &[0x73, 0xed, 0x00], // LD (HL), E
    |machine| {
      machine.cpu.regs.e = 0x42;
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x42);
}

#[test]
fn test_74() {
  let machine = run_test(
    &[0x74, 0xed, 0x42], // LD (HL), H
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x00);
}

#[test]
fn test_75() {
  let machine = run_test(
    &[0x75, 0xed, 0x00], // LD (HL), L
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x02);
}

#[test]
fn test_76() {
  let machine = run_test(
    &[0x76], // HALT
    |machine| {
      machine.cpu.ime = true;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.step, Step::Halt);
}

#[test]
fn test_77() {
  let machine = run_test(
    &[0x77, 0xed, 0x00], // LD (HL), A
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x42);
}

#[test]
fn test_78() {
  let machine = run_test(
    &[0x78], // LD A, B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_79() {
  let machine = run_test(
    &[0x79], // LD A, C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_7a() {
  let machine = run_test(
    &[0x7a], // LD A, D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_7b() {
  let machine = run_test(
    &[0x7b], // LD A, E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_7c() {
  let machine = run_test(
    &[0x7c], // LD A, H
    |machine| {
      machine.cpu.regs.h = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_7d() {
  let machine = run_test(
    &[0x7d], // LD A, L
    |machine| {
      machine.cpu.regs.l = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_7e() {
  let machine = run_test(
    &[0x7e, 0xed, 0x42], // LD A, (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_7f() {
  let machine = run_test(
    &[0x7f], // LD A, A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x42);
}
