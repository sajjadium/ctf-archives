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
use crate::cpu::test::run_test;

#[test]
fn test_c3() {
  let machine = run_test(
    &[0xc3, 0x04, 0x00, 0xed], // JP nn
    |_| {},
  );
  assert_eq!(machine.hardware.clock_cycles(), 16);
  assert_eq!(machine.cpu.regs.pc, 0x05);
}
