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
use num_traits::{PrimInt, WrappingAdd, WrappingSub};

#[cfg(test)]
use quickcheck::quickcheck;

pub trait IntExt {
  /// Isolates the rightmost 1-bit leaving all other bits as 0
  /// e.g. 1010 1000 -> 0000 1000
  ///
  /// Equivalent to Intel BMI1 instruction BLSI
  fn isolate_rightmost_one(self) -> Self;

  /// Returns the specified bit as 0 or 1
  fn bit(self, bit: usize) -> Self;

  /// Returns the specified bit as boolean
  fn bit_bool(self, bit: usize) -> bool;

  /// Sets all rightmost 0-bits to 1
  /// e.g. 1010 1000 -> 1010 1111
  ///
  /// Equivalent to Intel BMI1 instruction BLSMSK
  fn activate_rightmost_zeros(self) -> Self;

  /// Tests if addition results in a carry from the specified bit.
  /// Does not support overflow, so cannot be used to check carry from the leftmost bit
  fn test_add_carry_bit(bit: usize, a: Self, b: Self) -> bool;
}

impl<T> IntExt for T
where
  T: PrimInt + WrappingAdd + WrappingSub,
{
  /// Isolates the rightmost 1-bit leaving all other bits as 0
  /// e.g. 1010 1000 -> 0000 1000
  ///
  /// Equivalent to Intel BMI1 instruction BLSI
  #[inline(always)]
  fn isolate_rightmost_one(self) -> Self {
    let x = self;
    // Unsigned negation: -x == !x + 1
    let minus_x = (!x).wrapping_add(&Self::one());
    // Hacker's Delight 2nd ed, 2-1 Manipulating Rightmost Bits
    x & minus_x
  }

  /// Returns the specified bit as 0 or 1
  #[inline(always)]
  fn bit(self, bit: usize) -> Self {
    (self >> bit) & Self::one()
  }

  /// Returns the specified bit as boolean
  #[inline(always)]
  fn bit_bool(self, bit: usize) -> bool {
    !self.bit(bit).is_zero()
  }

  /// Sets all rightmost 0-bits to 1
  /// e.g. 1010 1000 -> 1010 1111
  ///
  /// Equivalent to Intel BMI1 instruction BLSMSK
  #[inline(always)]
  fn activate_rightmost_zeros(self) -> Self {
    let x = self;
    // Hacker's Delight 2nd ed, 2-1 Manipulating Rightmost Bits
    x | x.wrapping_sub(&Self::one())
  }

  /// Tests if addition results in a carry from the specified bit.
  /// Does not support overflow, so cannot be used to check carry from the leftmost bit
  #[inline(always)]
  fn test_add_carry_bit(bit: usize, a: Self, b: Self) -> bool {
    // Create a mask that includes the specified bit and 1-bits on the right side
    // e.g. for u8:
    //   bit=0 -> 0000 0001
    //   bit=3 -> 0000 1111
    //   bit=6 -> 0111 1111
    let mask = (Self::one() << bit).activate_rightmost_zeros();
    (a & mask) + (b & mask) > mask
  }
}

#[cfg(test)]
fn test_isolate_rightmost_one<T: PrimInt + WrappingAdd + WrappingSub>(x: T) -> bool {
  let y = x.isolate_rightmost_one();
  if x.is_zero() {
    y.is_zero()
  } else {
    let mut value = x;
    let mut expected = T::one();
    while !value.bit_bool(0) {
      value = value >> 1;
      expected = expected << 1;
    }
    y == expected
  }
}

#[cfg(test)]
#[test]
fn test_u8_isolate_rightmost_one() {
  fn prop(x: u8) -> bool {
    test_isolate_rightmost_one(x)
  }
  quickcheck(prop as fn(u8) -> bool);
}

#[cfg(test)]
#[test]
fn test_u16_isolate_rightmost_one() {
  fn prop(x: u16) -> bool {
    test_isolate_rightmost_one(x)
  }
  quickcheck(prop as fn(u16) -> bool);
}
