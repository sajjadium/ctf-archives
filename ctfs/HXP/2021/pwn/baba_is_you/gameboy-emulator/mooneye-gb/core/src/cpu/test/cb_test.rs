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

macro_rules! test_bit_r8(
  ($test: ident, $reg: ident, $bit: expr, $op: expr) => (
    #[test]
    fn $test() {
      {
        let machine = run_test(
          &[0xcb, $op],
          |machine| {
            machine.cpu.regs.$reg = 1 << $bit;
          }
        );
        assert_eq!(machine.hardware.clock_cycles(), 8);
        assert_eq!(machine.cpu.regs.f, Flags::HALF_CARRY);
      }
      {
        let machine = run_test(
          &[0xcb, $op],
          |machine| {
            machine.cpu.regs.$reg = 0;
          }
        );
        assert_eq!(machine.hardware.clock_cycles(), 8);
        assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::HALF_CARRY);
      }
    }
  );
);

macro_rules! test_bit_hl(
  ($test: ident, $bit: expr, $op: expr) => (
    #[test]
    fn $test() {
      {
        let machine = run_test(
          &[0xcb, $op, 0xed, 1 << $bit],
          |machine| {
            machine.cpu.regs.h = 0x00;
            machine.cpu.regs.l = 0x03;
          }
        );
        assert_eq!(machine.hardware.clock_cycles(), 12);
        assert_eq!(machine.cpu.regs.f, Flags::HALF_CARRY);
      }
      {
        let machine = run_test(
          &[0xcb, $op, 0xed, 0x00],
          |machine| {
            machine.cpu.regs.h = 0x00;
            machine.cpu.regs.l = 0x03;
          }
        );
        assert_eq!(machine.hardware.clock_cycles(), 12);
        assert_eq!(machine.cpu.regs.f, Flags::ZERO | Flags::HALF_CARRY);
      }
    }
  );
);

test_bit_r8!(test_bit0_a, a, 0, 0x47);
test_bit_r8!(test_bit1_a, a, 1, 0x4f);
test_bit_r8!(test_bit2_a, a, 2, 0x57);
test_bit_r8!(test_bit3_a, a, 3, 0x5f);
test_bit_r8!(test_bit4_a, a, 4, 0x67);
test_bit_r8!(test_bit5_a, a, 5, 0x6f);
test_bit_r8!(test_bit6_a, a, 6, 0x77);
test_bit_r8!(test_bit7_a, a, 7, 0x7f);

test_bit_r8!(test_bit0_b, b, 0, 0x40);
test_bit_r8!(test_bit1_b, b, 1, 0x48);
test_bit_r8!(test_bit2_b, b, 2, 0x50);
test_bit_r8!(test_bit3_b, b, 3, 0x58);
test_bit_r8!(test_bit4_b, b, 4, 0x60);
test_bit_r8!(test_bit5_b, b, 5, 0x68);
test_bit_r8!(test_bit6_b, b, 6, 0x70);
test_bit_r8!(test_bit7_b, b, 7, 0x78);

test_bit_r8!(test_bit0_c, c, 0, 0x41);
test_bit_r8!(test_bit1_c, c, 1, 0x49);
test_bit_r8!(test_bit2_c, c, 2, 0x51);
test_bit_r8!(test_bit3_c, c, 3, 0x59);
test_bit_r8!(test_bit4_c, c, 4, 0x61);
test_bit_r8!(test_bit5_c, c, 5, 0x69);
test_bit_r8!(test_bit6_c, c, 6, 0x71);
test_bit_r8!(test_bit7_c, c, 7, 0x79);

test_bit_r8!(test_bit0_d, d, 0, 0x42);
test_bit_r8!(test_bit1_d, d, 1, 0x4a);
test_bit_r8!(test_bit2_d, d, 2, 0x52);
test_bit_r8!(test_bit3_d, d, 3, 0x5a);
test_bit_r8!(test_bit4_d, d, 4, 0x62);
test_bit_r8!(test_bit5_d, d, 5, 0x6a);
test_bit_r8!(test_bit6_d, d, 6, 0x72);
test_bit_r8!(test_bit7_d, d, 7, 0x7a);

test_bit_r8!(test_bit0_e, e, 0, 0x43);
test_bit_r8!(test_bit1_e, e, 1, 0x4b);
test_bit_r8!(test_bit2_e, e, 2, 0x53);
test_bit_r8!(test_bit3_e, e, 3, 0x5b);
test_bit_r8!(test_bit4_e, e, 4, 0x63);
test_bit_r8!(test_bit5_e, e, 5, 0x6b);
test_bit_r8!(test_bit6_e, e, 6, 0x73);
test_bit_r8!(test_bit7_e, e, 7, 0x7b);

test_bit_r8!(test_bit0_h, h, 0, 0x44);
test_bit_r8!(test_bit1_h, h, 1, 0x4c);
test_bit_r8!(test_bit2_h, h, 2, 0x54);
test_bit_r8!(test_bit3_h, h, 3, 0x5c);
test_bit_r8!(test_bit4_h, h, 4, 0x64);
test_bit_r8!(test_bit5_h, h, 5, 0x6c);
test_bit_r8!(test_bit6_h, h, 6, 0x74);
test_bit_r8!(test_bit7_h, h, 7, 0x7c);

test_bit_r8!(test_bit0_l, l, 0, 0x45);
test_bit_r8!(test_bit1_l, l, 1, 0x4d);
test_bit_r8!(test_bit2_l, l, 2, 0x55);
test_bit_r8!(test_bit3_l, l, 3, 0x5d);
test_bit_r8!(test_bit4_l, l, 4, 0x65);
test_bit_r8!(test_bit5_l, l, 5, 0x6d);
test_bit_r8!(test_bit6_l, l, 6, 0x75);
test_bit_r8!(test_bit7_l, l, 7, 0x7d);

test_bit_hl!(test_bit0_hl, 0, 0x46);
test_bit_hl!(test_bit1_hl, 1, 0x4e);
test_bit_hl!(test_bit2_hl, 2, 0x56);
test_bit_hl!(test_bit3_hl, 3, 0x5e);
test_bit_hl!(test_bit4_hl, 4, 0x66);
test_bit_hl!(test_bit5_hl, 5, 0x6e);
test_bit_hl!(test_bit6_hl, 6, 0x76);
test_bit_hl!(test_bit7_hl, 7, 0x7e);
