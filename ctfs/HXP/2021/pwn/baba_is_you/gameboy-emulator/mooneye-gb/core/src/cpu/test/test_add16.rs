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
use crate::cpu::register_file::{Flags, Reg16};
use crate::cpu::test::run_test;

fn test_add16<F: Fn(Flags) -> bool>(
  opcode: u8,
  hl: u16,
  reg: Reg16,
  x: u16,
  check_flags: F,
) -> bool {
  let machine = run_test(&[opcode], |machine| {
    machine.cpu.regs.write16(Reg16::HL, hl);
    machine.cpu.regs.write16(reg, x);
  });
  let expected = hl.wrapping_add(x);
  machine.hardware.clock_cycles() == 8
    && machine.cpu.regs.read16(Reg16::HL) == expected
    && check_flags(machine.cpu.regs.f)
}

#[test]
fn test_09() {
  assert!(test_add16(0x09, 0x0003, Reg16::BC, 0x0ffc, |f| f == Flags::empty()));
}

#[test]
fn test_09_carry() {
  assert!(test_add16(0x09, 0x5002, Reg16::BC, 0xb7fd, |f| f == Flags::CARRY));
}

#[test]
fn test_09_gb_manual() {
  assert!(test_add16(0x09, 0x8a23, Reg16::BC, 0x0605, |f| f == Flags::HALF_CARRY));
}

#[test]
fn test_19() {
  assert!(test_add16(0x19, 0x0003, Reg16::DE, 0x0ffc, |f| f == Flags::empty()));
}

#[test]
fn test_19_half_carry() {
  assert!(test_add16(0x19, 0x8a23, Reg16::DE, 0x0605, |f| f == Flags::HALF_CARRY));
}

#[test]
fn test_19_carry() {
  assert!(test_add16(0x19, 0x5002, Reg16::DE, 0xb7fd, |f| f == Flags::CARRY));
}

#[test]
fn test_29() {
  assert!(test_add16(0x29, 0x02aa, Reg16::HL, 0x02aa, |f| f == Flags::empty()));
}

#[test]
fn test_29_half_carry() {
  assert!(test_add16(0x29, 0x0fff, Reg16::HL, 0x0fff, |f| f == Flags::HALF_CARRY));
}

#[test]
fn test_29_carry() {
  assert!(test_add16(0x29, 0x8001, Reg16::HL, 0x8001, |f| f == Flags::CARRY));
}

#[test]
fn test_29_gb_manual() {
  assert!(test_add16(0x29, 0x8a23, Reg16::HL, 0x8a23, |f| f
    == Flags::HALF_CARRY | Flags::CARRY));
}

#[test]
fn test_39() {
  assert!(test_add16(0x39, 0x0003, Reg16::SP, 0x0ffc, |f| f == Flags::empty()));
}

#[test]
fn test_39_half_carry() {
  assert!(test_add16(0x39, 0x8a23, Reg16::SP, 0x0605, |f| f == Flags::HALF_CARRY));
}

#[test]
fn test_39_carry() {
  assert!(test_add16(0x39, 0x5002, Reg16::SP, 0xb7fd, |f| f == Flags::CARRY));
}
