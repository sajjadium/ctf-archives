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
fn test_30() {
  let machine = run_test(
    &[0x30, 0x01, 0xed, 0xed], // JR NC, e
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.cpu.regs.pc, 0x04);
}

#[test]
fn test_30_negative() {
  let machine = run_test(
    &[0x00, 0xed, 0x30, -3i8 as u8], // JR NC, e
    |machine| {
      machine.cpu.regs.pc = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.cpu.regs.pc, 0x02);
}

#[test]
fn test_30_nojump() {
  let machine = run_test(
    &[0x30, 0x01, 0xed, 0x00], // JR NC, e
    |machine| {
      machine.cpu.regs.f = Flags::CARRY;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.pc, 0x03);
}

#[test]
fn test_32() {
  let machine = run_test(
    &[0x32, 0xed, 0x00], // LDD (HL), A
    |machine| {
      machine.cpu.regs.a = 0x42;
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.h, 0x00);
  assert_eq!(machine.cpu.regs.l, 0x01);
  assert_eq!(machine.hardware.memory[0x02], 0x42);
}

#[test]
fn test_34() {
  let machine = run_test(
    &[0x34, 0xed, 0x42], // INC (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.hardware.memory[0x02], 0x43);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_34_zero() {
  let machine = run_test(
    &[0x34, 0xed, 0xff], // INC (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.hardware.memory[0x02], 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::HALF_CARRY);
}

#[test]
fn test_34_half_carry() {
  let machine = run_test(
    &[0x34, 0xed, 0x0f], // INC (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.hardware.memory[0x02], 0x10);
  assert_eq!(machine.cpu.regs.f, Flags::HALF_CARRY);
}

#[test]
fn test_35() {
  let machine = run_test(
    &[0x35, 0xed, 0x42], // DEC (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.hardware.memory[0x02], 0x41);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT);
}

#[test]
fn test_35_zero() {
  let machine = run_test(
    &[0x35, 0xed, 0x01], // DEC (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.hardware.memory[0x02], 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::ADD_SUBTRACT);
}

#[test]
fn test_35_half_carry() {
  let machine = run_test(
    &[0x35, 0xed, 0x00], // DEC (HL)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.hardware.memory[0x02], 0xff);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT | Flags::HALF_CARRY);
}

#[test]
fn test_36() {
  let machine = run_test(
    &[0x36, 0x42, 0xed, 0x00], // LD (HL), n
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x03;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.hardware.memory[0x03], 0x42);
}

#[test]
fn test_37() {
  let machine = run_test(
    &[0x37], // SCF
    |machine| {
      machine.cpu.regs.f = Flags::ADD_SUBTRACT | Flags::HALF_CARRY;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.f, Flags::CARRY);
}

#[test]
fn test_38() {
  let machine = run_test(
    &[0x38, 0x01, 0xed, 0xed], // JR C, e
    |machine| {
      machine.cpu.regs.f = Flags::CARRY;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.cpu.regs.pc, 0x04);
}

#[test]
fn test_38_negative() {
  let machine = run_test(
    &[0x00, 0xed, 0x38, -3i8 as u8], // JR C, e
    |machine| {
      machine.cpu.regs.f = Flags::CARRY;
      machine.cpu.regs.pc = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 12);
  assert_eq!(machine.cpu.regs.pc, 0x02);
}

#[test]
fn test_38_nojump() {
  let machine = run_test(
    &[0x38, 0x01, 0xed, 0x00], // JR C, e
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.pc, 0x03);
}

#[test]
fn test_3a() {
  let machine = run_test(
    &[0x3a, 0xed, 0x42], // LD A, (HL-)
    |machine| {
      machine.cpu.regs.h = 0x00;
      machine.cpu.regs.l = 0x02;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x42);
  assert_eq!(machine.cpu.regs.h, 0x00);
  assert_eq!(machine.cpu.regs.l, 0x01);
}

#[test]
fn test_3c() {
  let machine = run_test(
    &[0x3c], // INC A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x43);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}

#[test]
fn test_3c_zero() {
  let machine = run_test(
    &[0x3c], // INC A
    |machine| {
      machine.cpu.regs.a = 0xff;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::HALF_CARRY);
}

#[test]
fn test_3c_half_carry() {
  let machine = run_test(
    &[0x3c], // INC A
    |machine| {
      machine.cpu.regs.a = 0x0f;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x10);
  assert_eq!(machine.cpu.regs.f, Flags::HALF_CARRY);
}

#[test]
fn test_3d() {
  let machine = run_test(
    &[0x3d], // DEC A
    |machine| {
      machine.cpu.regs.a = 0x42;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x41);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT);
}

#[test]
fn test_3d_zero() {
  let machine = run_test(
    &[0x3d], // DEC A
    |machine| {
      machine.cpu.regs.a = 0x01;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0x00);
  assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::ADD_SUBTRACT);
}

#[test]
fn test_3d_half_carry() {
  let machine = run_test(
    &[0x3d], // DEC A
    |machine| {
      machine.cpu.regs.a = 0x00;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.a, 0xff);
  assert_eq!(machine.cpu.regs.f, Flags::ADD_SUBTRACT | Flags::HALF_CARRY);
}

#[test]
fn test_3e() {
  let machine = run_test(
    &[0x3e, 0x42], // LD A, n
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 8);
  assert_eq!(machine.cpu.regs.a, 0x42);
}

#[test]
fn test_3f() {
  let machine = run_test(
    &[0x3f], // CCF
    |machine| {
      machine.cpu.regs.f = Flags::ADD_SUBTRACT | Flags::HALF_CARRY;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.f, Flags::CARRY);
}

#[test]
fn test_3f_carry() {
  let machine = run_test(
    &[0x3f], // CCF
    |machine| {
      machine.cpu.regs.f = Flags::ADD_SUBTRACT | Flags::HALF_CARRY | Flags::CARRY;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 4);
  assert_eq!(machine.cpu.regs.f, Flags::empty());
}
