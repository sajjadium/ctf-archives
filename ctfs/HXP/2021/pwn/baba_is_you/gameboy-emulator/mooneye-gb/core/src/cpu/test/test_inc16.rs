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

fn test_inc16(opcode: u8, x: u16, reg: Reg16) -> bool {
  let machine = run_test(&[opcode], |machine| {
    machine.cpu.regs.write16(reg, x);
  });
  let expected = x.wrapping_add(1);
  machine.hardware.clock_cycles() == 8 && machine.cpu.regs.read16(reg) == expected
}

#[test]
fn test_03() {
  fn prop(x: u16) -> bool {
    test_inc16(0x03, x, Reg16::BC)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_03_overflow() {
  assert!(test_inc16(0x03, 0xffff, Reg16::BC))
}

#[test]
fn test_13() {
  fn prop(x: u16) -> bool {
    test_inc16(0x13, x, Reg16::DE)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_13_overflow() {
  assert!(test_inc16(0x13, 0xffff, Reg16::DE))
}

#[test]
fn test_23() {
  fn prop(x: u16) -> bool {
    test_inc16(0x23, x, Reg16::HL)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_23_overflow() {
  assert!(test_inc16(0x23, 0xffff, Reg16::HL))
}

#[test]
fn test_33() {
  fn prop(x: u16) -> bool {
    test_inc16(0x33, x, Reg16::SP)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_33_overflow() {
  assert!(test_inc16(0x33, 0xffff, Reg16::SP))
}
