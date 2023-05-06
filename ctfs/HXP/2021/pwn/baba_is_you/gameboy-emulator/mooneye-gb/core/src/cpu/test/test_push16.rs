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

fn test_push16(opcode: u8, reg: Reg16, x: u16) -> bool {
  let machine = run_test(&[opcode, 0xed, 0x00, 0x00], |machine| {
    machine.cpu.regs.write16(reg, x);
    machine.cpu.regs.sp = 0x0004;
  });
  machine.hardware.clock_cycles() == 16
    && machine.cpu.regs.sp == 0x0002
    && machine.hardware.memory[0x03] == (x >> 8) as u8
    && machine.hardware.memory[0x02] == (x as u8)
}

#[test]
fn test_c5() {
  fn prop(x: u16) -> bool {
    test_push16(0xc5, Reg16::BC, x)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_d5() {
  fn prop(x: u16) -> bool {
    test_push16(0xd5, Reg16::DE, x)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_e5() {
  fn prop(x: u16) -> bool {
    test_push16(0xe5, Reg16::HL, x)
  }
  quickcheck(prop as fn(u16) -> bool);
}

#[test]
fn test_f5() {
  fn prop(a: u8, f: u8) -> bool {
    let machine = run_test(&[0xf5, 0xed, 0x00, 0x00], |machine| {
      machine.cpu.regs.a = a;
      machine.cpu.regs.f = Flags::from_bits_truncate(f);
      machine.cpu.regs.sp = 0x0004;
    });
    machine.hardware.clock_cycles() == 16
      && machine.cpu.regs.sp == 0x0002
      && machine.hardware.memory[0x03] == a
      && machine.hardware.memory[0x02] == (f & 0xF0)
  }
  quickcheck(prop as fn(u8, u8) -> bool);
}
