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

#[test]
fn test_f9() {
  fn prop(hl: u16) -> bool {
    let machine = run_test(&[0xf9], |machine| {
      machine.cpu.regs.write16(Reg16::HL, hl);
    });
    machine.hardware.clock_cycles() == 8 && machine.cpu.regs.read16(Reg16::SP) == hl
  }
  quickcheck(prop as fn(u16) -> bool);
}
