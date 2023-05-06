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
use bitflags::bitflags;
use std::fmt;
use std::fmt::{Binary, Formatter, LowerHex, UpperHex};

use crate::hardware::interrupts::{InterruptLine, InterruptRequest, Interrupts};
use crate::GbKey;

/// Gameboy joypad.
///
/// Gameboy has a dpad, and four buttons: A, B, Select, Start.
/// From a program's point of view there are two ways to interact with it:
///
/// # Joypad register (P1)
/// The joypad register can be used to access the state of four keys at a time.
///
/// # Joypad interrupt
/// Whenever a key is pressed, a joypad interrupt is requested.
#[derive(Clone)]
pub struct Joypad {
  pressed_directional: P1,
  pressed_button: P1,
  register: P1,
}

impl Joypad {
  pub fn new() -> Joypad {
    Joypad {
      pressed_directional: P1::empty(),
      pressed_button: P1::empty(),
      register: P1::INITIAL_STATE,
    }
  }

  pub fn get_register(&self) -> u8 {
    // Invert bits, so 0 means "set". Unused bits in P1 are 0,
    // so they automatically become 1 and no mask is needed
    !self.register.bits
  }
  pub fn set_register(&mut self, value: u8) {
    // Invert bits before converting to P1
    self.register = P1::from_bits_truncate(!value);
    self.update_register();
  }

  pub fn key_down(&mut self, key: GbKey, interrupts: &mut Interrupts) {
    self.pressed_directional.insert(P1::directional(&key));
    self.pressed_button.insert(P1::button(&key));
    self.update_register();
    interrupts.request_t12_interrupt(InterruptLine::JOYPAD);
  }
  pub fn key_up(&mut self, key: GbKey) {
    self.pressed_directional.remove(P1::directional(&key));
    self.pressed_button.remove(P1::button(&key));
    self.update_register();
  }

  /// Updates the register state based on select bits P14-P15 and the
  /// pressed buttons
  fn update_register(&mut self) {
    self.register &= P1::WRITABLE;
    if self.register.contains(P1::SELECT_DIRECTIONAL) {
      self.register.insert(self.pressed_directional);
    }
    if self.register.contains(P1::SELECT_BUTTON) {
      self.register.insert(self.pressed_button);
    }
  }
}

impl Binary for Joypad {
  fn fmt(&self, f: &mut Formatter) -> fmt::Result {
    write!(f, "{:08b}", !self.register.bits)
  }
}
impl LowerHex for Joypad {
  fn fmt(&self, f: &mut Formatter) -> fmt::Result {
    write!(f, "{:02x}", !self.register.bits)
  }
}
impl UpperHex for Joypad {
  fn fmt(&self, f: &mut Formatter) -> fmt::Result {
    write!(f, "{:02X}", !self.register.bits)
  }
}

bitflags!(
  /// P1 register
  ///
  /// Bits are inverted in get_register/set_register, so in P1
  /// a set bit is 1 as usual.
  struct P1: u8 {
    const P10                = 1 << 0; // P10: →, A
    const P11                = 1 << 1; // P11: ←, B
    const P12                = 1 << 2; // P12: ↑, Select
    const P13                = 1 << 3; // P13: ↓, Start
    const SELECT_DIRECTIONAL = 1 << 4; // P14: Select dpad
    const SELECT_BUTTON      = 1 << 5; // P15: Select buttons

    /// Only select bits are writable
    const WRITABLE =
      P1::SELECT_DIRECTIONAL.bits | P1::SELECT_BUTTON.bits;

    /// DMG: initial state 0xCF
    /// See docs/accuracy/joypad.markdown
    const INITIAL_STATE = P1::WRITABLE.bits;
  }
);

impl P1 {
  fn directional(key: &GbKey) -> P1 {
    match *key {
      GbKey::Right => P1::P10,
      GbKey::Left => P1::P11,
      GbKey::Up => P1::P12,
      GbKey::Down => P1::P13,
      _ => P1::empty(),
    }
  }
  fn button(key: &GbKey) -> P1 {
    match *key {
      GbKey::A => P1::P10,
      GbKey::B => P1::P11,
      GbKey::Select => P1::P12,
      GbKey::Start => P1::P13,
      _ => P1::empty(),
    }
  }
}
