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

fn test_load16_hl_sp_e<F: Fn(Flags) -> bool>(sp: u16, e: i8, check_flags: F) -> bool {
  let machine = run_test(&[0xf8, e as u8], |machine| {
    machine.cpu.regs.write16(Reg16::SP, sp);
  });
  let expected = sp.wrapping_add(e as i16 as u16);
  machine.hardware.clock_cycles() == 12
    && machine.cpu.regs.read16(Reg16::HL) == expected
    && check_flags(machine.cpu.regs.f)
}

#[test]
fn test_f8() {
  fn prop(sp: u16, e: i8) -> bool {
    test_load16_hl_sp_e(sp, e, |_| true)
  }
  quickcheck(prop as fn(u16, i8) -> bool);
}

#[test]
fn test_f8_overflow_inc() {
  assert!(test_load16_hl_sp_e(0xffff, 1, |f| f == Flags::HALF_CARRY | Flags::CARRY));
}

#[test]
fn test_f8_overflow_dec() {
  assert!(test_load16_hl_sp_e(0x0000, -1, |f| f == Flags::empty()));
}
