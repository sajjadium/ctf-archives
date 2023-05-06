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

use crate::cpu::register_file::{Flags, Reg16};
use crate::cpu::test::run_test;

fn test_pop16(opcode: u8, x: u16, reg: Reg16) -> bool {
  let h = (x >> 8) as u8;
  let l = x as u8;
  let machine = run_test(&[opcode, 0xed, l, h], |machine| {
    machine.cpu.regs.sp = 0x0002;
  });
  machine.hardware.clock_cycles() == 12
    && machine.cpu.regs.sp == 0x0004
    && machine.cpu.regs.read16(reg) == x
}

#[test]
fn test_c1() {
  fn prop(x: u16) -> bool {
    test_pop16(0xc1, x, Reg16::BC)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_d1() {
  fn prop(x: u16) -> bool {
    test_pop16(0xd1, x, Reg16::DE)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_e1() {
  fn prop(x: u16) -> bool {
    test_pop16(0xe1, x, Reg16::HL)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_f1() {
  fn prop(a: u8, f: u8) -> bool {
    let machine = run_test(&[0xf1, 0xed, f, a], |machine| {
      machine.cpu.regs.sp = 0x0002;
    });
    machine.hardware.clock_cycles() == 12
      && machine.cpu.regs.a == a
      && machine.cpu.regs.f == Flags::from_bits_truncate(f)
  }
  quickcheck(prop as fn(u8, u8) -> bool);
}
