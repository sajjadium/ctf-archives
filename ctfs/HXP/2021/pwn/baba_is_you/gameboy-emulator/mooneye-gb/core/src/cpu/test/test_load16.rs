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

fn test_load16(opcode: u8, x: u16, reg: Reg16) -> bool {
  let h = (x >> 8) as u8;
  let l = x as u8;
  let machine = run_test(&[opcode, l, h], |_| {});
  machine.hardware.clock_cycles() == 12 && machine.cpu.regs.read16(reg) == x
}

#[test]
fn test_01() {
  fn prop(x: u16) -> bool {
    test_load16(0x01, x, Reg16::BC)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_11() {
  fn prop(x: u16) -> bool {
    test_load16(0x11, x, Reg16::DE)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_21() {
  fn prop(x: u16) -> bool {
    test_load16(0x21, x, Reg16::HL)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_31() {
  fn prop(x: u16) -> bool {
    test_load16(0x31, x, Reg16::SP)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_08() {
  let machine = run_test(
    &[0x08, 0x04, 0x00, 0xed, 0x00, 0x00], // LD (nn), SP
    |machine| {
      machine.cpu.regs.sp = 0x8042;
    },
  );
  assert_eq!(machine.hardware.clock_cycles(), 20);
  assert_eq!(machine.hardware.memory[0x04], 0x42);
  assert_eq!(machine.hardware.memory[0x05], 0x80);
}
