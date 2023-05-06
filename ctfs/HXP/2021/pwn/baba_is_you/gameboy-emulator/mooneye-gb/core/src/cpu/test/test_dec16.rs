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
use quickcheck::quickcheck;

use crate::cpu::register_file::Reg16;
use crate::cpu::test::run_test;

fn test_dec16(opcode: u8, x: u16, reg: Reg16) -> bool {
  let machine = run_test(&[opcode], |machine| {
    machine.cpu.regs.write16(reg, x);
  });
  let expected = x.wrapping_sub(1);
  machine.hardware.clock_cycles() == 8 && machine.cpu.regs.read16(reg) == expected
}

#[test]
fn test_0b() {
  fn prop(x: u16) -> bool {
    test_dec16(0x0b, x, Reg16::BC)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_0b_overflow() {
  assert!(test_dec16(0x0b, 0x0000, Reg16::BC))
}

#[test]
fn test_1b() {
  fn prop(x: u16) -> bool {
    test_dec16(0x1b, x, Reg16::DE)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_1b_overflow() {
  assert!(test_dec16(0x1b, 0x0000, Reg16::DE))
}

#[test]
fn test_2b() {
  fn prop(x: u16) -> bool {
    test_dec16(0x2b, x, Reg16::HL)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_2b_overflow() {
  assert!(test_dec16(0x2b, 0x0000, Reg16::HL))
}

#[test]
fn test_3b() {
  fn prop(x: u16) -> bool {
    test_dec16(0x3b, x, Reg16::SP)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_3b_overflow() {
  assert!(test_dec16(0x3b, 0x0000, Reg16::SP))
}
