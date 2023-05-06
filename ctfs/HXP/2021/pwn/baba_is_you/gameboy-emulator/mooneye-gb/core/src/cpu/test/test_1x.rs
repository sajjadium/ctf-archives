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
fn test_12() {
  let machine = run_test(
    &[0x12, 0xed, 0x00], // LD (DE), A
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.d = 0x00;
      machine.cpu.regs.e = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.hardware.memory[0x02], 0x42);
}

#[test]
fn test_14() {
  let machine = run_test(
    &[0x14], // INC D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x43);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_14_zero() {
  let machine = run_test(
    &[0x14], // INC D
    |machine| {
      machine.cpu.regs.d = 0xff;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::HALF_CARRY);
}

#[test]
fn test_14_half_carry() {
  let machine = run_test(
    &[0x14], // INC D
    |machine| {
      machine.cpu.regs.d = 0x0f;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x10);
  assert_eq!(machine.cpu.regs.f, Flags::HALF_CARRY);
}

#[test]
fn test_15() {
  let machine = run_test(
    &[0x15], // DEC D
    |machine| {
      machine.cpu.regs.d = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x41);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT);
}

#[test]
fn test_15_zero() {
  let machine = run_test(
    &[0x15], // DEC D
    |machine| {
      machine.cpu.regs.d = 0x01;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::ADD_SUBTRACT);
}

#[test]
fn test_15_half_carry() {
  let machine = run_test(
    &[0x15], // DEC D
    |machine| {
      machine.cpu.regs.d = 0x00;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.d, 0xff);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT | Flags::HALF_CARRY);
}

#[test]
fn test_16() {
  let machine = run_test(
    &[0x16, 0x42], // LD D, n
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.d, 0x42);
}

#[test]
fn test_17() {
  let machine = run_test(
    &[0x17], // RLA
    |machine| {
      machine.cpu.regs.a = 0x55;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0xaa);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_17_carry() {
  let machine = run_test(
    &[0x17], // RLA
    |machine| {
      machine.cpu.regs.a = 0xaa;
      machine.cpu.regs.f = Flags::CARRY;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x55);
  assert_eq!(machine.cpu.regs.f, Flags::CARRY);
}

#[test]
fn test_1a() {
  let machine = run_test(
    &[0x1a, 0xed, 0x42], // LD A, (DE)
    |machine| {
      machine.cpu.regs.d = 0x00;
      machine.cpu.regs.e = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_1c() {
  let machine = run_test(
    &[0x1c], // INC E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x43);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_1c_zero() {
  let machine = run_test(
    &[0x1c], // INC E
    |machine| {
      machine.cpu.regs.e = 0xff;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::HALF_CARRY);
}

#[test]
fn test_1c_half_carry() {
  let machine = run_test(
    &[0x1c], // INC E
    |machine| {
      machine.cpu.regs.e = 0x0f;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x10);
  assert_eq!(machine.cpu.regs.f, Flags::HALF_CARRY);
}

#[test]
fn test_1d() {
  let machine = run_test(
    &[0x1d], // DEC E
    |machine| {
      machine.cpu.regs.e = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x41);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT);
}

#[test]
fn test_1d_zero() {
  let machine = run_test(
    &[0x1d], // DEC E
    |machine| {
      machine.cpu.regs.e = 0x01;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::ADD_SUBTRACT);
}

#[test]
fn test_1d_half_carry() {
  let machine = run_test(
    &[0x1d], // DEC E
    |machine| {
      machine.cpu.regs.e = 0x00;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.e, 0xff);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT | Flags::HALF_CARRY);
}

#[test]
fn test_1e() {
  let machine = run_test(
    &[0x1e, 0x42], // LD E, n
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.e, 0x42);
}

#[test]
fn test_1f() {
  let machine = run_test(
    &[0x1f], // RRA
    |machine| {
      machine.cpu.regs.a = 0xaa;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x55);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_1f_carry() {
  let machine = run_test(
    &[0x1f], // RRA
    |machine| {
      machine.cpu.regs.a = 0x55;
      machine.cpu.regs.f = Flags::CARRY;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0xaa);
  assert_eq!(machine.cpu.regs.f, Flags::CARRY);
}
