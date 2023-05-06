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
fn test_00() {
  let machine = run_test(
    &[0x00], // NOP
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
}

#[test]
fn test_02() {
  let machine = run_test(
    &[0x02, 0xed, 0x00], // LD (BC), A
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.b = 0x00;
      machine.cpu.regs.c = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x42);
}

#[test]
fn test_04() {
  let machine = run_test(
    &[0x04], // INC B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x43);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_04_zero() {
  let machine = run_test(
    &[0x04], // INC B
    |machine| {
      machine.cpu.regs.b = 0xff;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::HALF_CARRY);
}

#[test]
fn test_04_half_carry() {
  let machine = run_test(
    &[0x04], // INC B
    |machine| {
      machine.cpu.regs.b = 0x0f;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x10);
  assert_eq!(machine.cpu.regs.f, Flags::HALF_CARRY);
}

#[test]
fn test_05() {
  let machine = run_test(
    &[0x05], // DEC B
    |machine| {
      machine.cpu.regs.b = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x41);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT);
}

#[test]
fn test_05_zero() {
  let machine = run_test(
    &[0x05], // DEC B
    |machine| {
      machine.cpu.regs.b = 0x01;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::ADD_SUBTRACT);
}

#[test]
fn test_05_half_carry() {
  let machine = run_test(
    &[0x05], // DEC B
    |machine| {
      machine.cpu.regs.b = 0x00;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.b, 0xff);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT | Flags::HALF_CARRY);
}

#[test]
fn test_06() {
  let machine = run_test(
    &[0x06, 0x42], // LD B, n
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.b, 0x42);
}

#[test]
fn test_07() {
  let machine = run_test(
    &[0x07], // RLCA
    |machine| {
      machine.cpu.regs.a = 0x77;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0xee);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_07_carry() {
  let machine = run_test(
    &[0x07], // RLCA
    |machine| {
      machine.cpu.regs.a = 0xf7;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0xef);
  assert_eq!(machine.cpu.regs.f, Flags::CARRY);
}

#[test]
fn test_0a() {
  let machine = run_test(
    &[0x0a, 0xed, 0x42], // LD A, (BC)
    |machine| {
      machine.cpu.regs.b = 0x00;
      machine.cpu.regs.c = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_0c() {
  let machine = run_test(
    &[0x0c], // INC C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x43);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_0c_zero() {
  let machine = run_test(
    &[0x0c], // INC C
    |machine| {
      machine.cpu.regs.c = 0xff;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::HALF_CARRY);
}

#[test]
fn test_0c_half_carry() {
  let machine = run_test(
    &[0x0c], // INC C
    |machine| {
      machine.cpu.regs.c = 0x0f;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x10);
  assert_eq!(machine.cpu.regs.f, Flags::HALF_CARRY);
}

#[test]
fn test_0d() {
  let machine = run_test(
    &[0x0d], // DEC C
    |machine| {
      machine.cpu.regs.c = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x41);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT);
}

#[test]
fn test_0d_zero() {
  let machine = run_test(
    &[0x0d], // DEC C
    |machine| {
      machine.cpu.regs.c = 0x01;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::ADD_SUBTRACT);
}

#[test]
fn test_0d_half_carry() {
  let machine = run_test(
    &[0x0d], // DEC C
    |machine| {
      machine.cpu.regs.c = 0x00;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.c, 0xff);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT | Flags::HALF_CARRY);
}

#[test]
fn test_0e() {
  let machine = run_test(
    &[0x0e, 0x42], // LD C, n
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.c, 0x42);
}

#[test]
fn test_0f() {
  let machine = run_test(
    &[0x0f], // RRCA
    |machine| {
      machine.cpu.regs.a = 0xee;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x77);
  assert!(!machine.cpu.regs.f.contains(Flags::CARRY));
}

#[test]
fn test_0f_carry() {
  let machine = run_test(
    &[0x0f], // RRCA
    |machine| {
      machine.cpu.regs.a = 0xef;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0xf7);
  assert!(machine.cpu.regs.f.contains(Flags::CARRY));
}
