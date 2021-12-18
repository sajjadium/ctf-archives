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
use arrayvec::ArrayVec;
use bitflags::bitflags;
use std::cmp::Ordering;
use std::fmt;

use crate::emulation::EmuEvents;
use crate::gameboy;
use crate::gameboy::Color;
use crate::hardware::interrupts::{InterruptLine, InterruptRequest};
use crate::util::int::IntExt;
use crate::CoreContext;

const ACCESS_OAM_CYCLES: isize = 21;
const ACCESS_VRAM_CYCLES: isize = 43;
const HBLANK_CYCLES: isize = 50;
const VBLANK_LINE_CYCLES: isize = 114;
const UNDEFINED_READ: u8 = 0xff;
const STAT_UNUSED_MASK: u8 = (1 << 7);

#[derive(Clone)]
pub struct Ppu {
  control: Control,
  stat: Stat,
  current_line: u8,
  compare_line: u8,
  scroll_x: u8,
  scroll_y: u8,
  window_x: u8,
  window_y: u8,
  bg_palette: Palette,
  obj_palette0: Palette,
  obj_palette1: Palette,
  mode: Mode,
  cycles: isize,
  vram: Box<[u8; 0x2000]>,
  oam: Box<[u8; 0x100]>,
  pub back_buffer: Box<gameboy::ScreenBuffer>,
}

#[derive(Clone, Copy)]
struct Sprite {
  x: u8,
  y: u8,
  tile_num: u8,
  flags: SpriteFlags,
}

bitflags!(
  struct SpriteFlags: u8 {
    const UNUSED_MASK = 0b_0000_1111;
    const PALETTE     = 0b_0001_0000;
    const FLIPX       = 0b_0010_0000;
    const FLIPY       = 0b_0100_0000;
    const PRIORITY    = 0b_1000_0000;
  }
);

#[derive(Clone)]
struct Palette {
  off: Color,
  light: Color,
  dark: Color,
  on: Color,
  bits: u8,
}

impl Palette {
  fn new() -> Palette {
    Palette {
      off: Color::On,
      light: Color::On,
      dark: Color::On,
      on: Color::On,
      bits: 0xff,
    }
  }
  fn get(&self, color: &Color) -> Color {
    match *color {
      Color::Off => self.off,
      Color::Light => self.light,
      Color::Dark => self.dark,
      Color::On => self.on,
    }
  }
  fn set_bits(&mut self, value: u8) {
    self.off = Color::from_u8((value >> 0) & 0x3);
    self.light = Color::from_u8((value >> 2) & 0x3);
    self.dark = Color::from_u8((value >> 4) & 0x3);
    self.on = Color::from_u8((value >> 6) & 0x3);
    self.bits = value;
  }
}

bitflags!(
  struct Control: u8 {
    const BG_ON = 1 << 0;
    const OBJ_ON = 1 << 1;
    const OBJ_SIZE = 1 << 2;
    const BG_MAP = 1 << 3;
    const BG_ADDR = 1 << 4;
    const WINDOW_ON = 1 << 5;
    const WINDOW_MAP = 1 << 6;
    const LCD_ON = 1 << 7;
  }
);

bitflags!(
  struct Stat: u8 {
    const COMPARE = 1 << 2;
    const HBLANK_INT = 1 << 3;
    const VBLANK_INT = 1 << 4;
    const ACCESS_OAM_INT = 1 << 5;
    const COMPARE_INT = 1 << 6;
  }
);

#[derive(Copy, Clone, PartialEq, Eq)]
enum Mode {
  AccessOam,
  AccessVram,
  HBlank,
  VBlank,
}

impl Mode {
  fn cycles(&self, scroll_x: u8) -> isize {
    // FIXME: This is basically an ugly hack to pass a test. Most likely we don't just want
    // to adjust the cycle counts, but to actually emulate the behaviour that causes the adjustment
    let scroll_adjust = match scroll_x % 0x08 {
      5..=7 => 2,
      1..=4 => 1,
      _ => 0,
    };
    match *self {
      Mode::AccessOam => ACCESS_OAM_CYCLES,
      Mode::AccessVram => ACCESS_VRAM_CYCLES + scroll_adjust,
      Mode::HBlank => HBLANK_CYCLES - scroll_adjust,
      Mode::VBlank => VBLANK_LINE_CYCLES,
    }
  }
  fn bits(&self) -> u8 {
    match *self {
      Mode::AccessOam => 2,
      Mode::AccessVram => 3,
      Mode::HBlank => 0,
      Mode::VBlank => 1,
    }
  }
}

impl Ppu {
  pub fn new() -> Ppu {
    Ppu {
      control: Control::empty(),
      stat: Stat::empty(),
      current_line: 0,
      compare_line: 0,
      scroll_x: 0,
      scroll_y: 0,
      window_x: 0,
      window_y: 0,
      bg_palette: Palette::new(),
      obj_palette0: Palette::new(),
      obj_palette1: Palette::new(),
      mode: Mode::AccessOam,
      cycles: ACCESS_OAM_CYCLES,
      vram: Box::new([0; 0x2000]),
      oam: Box::new([0; 0x100]),
      back_buffer: Box::new(gameboy::SCREEN_EMPTY),
    }
  }
  pub fn get_control(&self) -> u8 {
    self.control.bits
  }
  pub fn get_stat(&self) -> u8 {
    if !self.control.contains(Control::LCD_ON) {
      STAT_UNUSED_MASK
    } else {
      self.mode.bits() | self.stat.bits | STAT_UNUSED_MASK
    }
  }
  pub fn get_scroll_y(&self) -> u8 {
    self.scroll_y
  }
  pub fn get_scroll_x(&self) -> u8 {
    self.scroll_x
  }
  pub fn get_current_line(&self) -> u8 {
    self.current_line
  }
  pub fn get_compare_line(&self) -> u8 {
    self.compare_line
  }
  pub fn get_bg_palette(&self) -> u8 {
    self.bg_palette.bits
  }
  pub fn get_obj_palette0(&self) -> u8 {
    self.obj_palette0.bits
  }
  pub fn get_obj_palette1(&self) -> u8 {
    self.obj_palette1.bits
  }
  pub fn get_window_x(&self) -> u8 {
    self.window_x
  }
  pub fn get_window_y(&self) -> u8 {
    self.window_y
  }
  pub fn set_control(&mut self, value: u8) {
    let new_control = Control::from_bits_truncate(value);
    if !new_control.contains(Control::LCD_ON) && self.control.contains(Control::LCD_ON) {
      if self.mode != Mode::VBlank {
        panic!("Warning! LCD off, but not in VBlank");
      }
      self.current_line = 0;
    }
    if new_control.contains(Control::LCD_ON) && !self.control.contains(Control::LCD_ON) {
      self.mode = Mode::HBlank;
      self.cycles = Mode::AccessOam.cycles(self.scroll_x);
      self.stat.insert(Stat::COMPARE);
    }
    self.control = new_control;
  }
  pub fn set_stat(&mut self, value: u8) {
    let new_stat = Stat::from_bits_truncate(value);
    self.stat = (self.stat & Stat::COMPARE)
      | (new_stat & Stat::HBLANK_INT)
      | (new_stat & Stat::VBLANK_INT)
      | (new_stat & Stat::ACCESS_OAM_INT)
      | (new_stat & Stat::COMPARE_INT);
  }
  pub fn set_scroll_y(&mut self, value: u8) {
    self.scroll_y = value;
  }
  pub fn set_scroll_x(&mut self, value: u8) {
    self.scroll_x = value;
  }
  pub fn reset_current_line(&mut self) {
    self.current_line = 0;
  }
  pub fn set_compare_line(&mut self, value: u8) {
    self.compare_line = value;
  }
  pub fn set_bg_palette(&mut self, value: u8) {
    self.bg_palette.set_bits(value);
  }
  pub fn set_obj_palette0(&mut self, value: u8) {
    self.obj_palette0.set_bits(value);
  }
  pub fn set_obj_palette1(&mut self, value: u8) {
    self.obj_palette1.set_bits(value);
  }
  pub fn set_window_x(&mut self, value: u8) {
    self.window_x = value;
  }
  pub fn set_window_y(&mut self, value: u8) {
    self.window_y = value;
  }
  pub fn write_video_ram(&mut self, addr: u16, value: u8) {
    if self.mode == Mode::AccessVram {
      return;
    }
    self.vram[(addr as usize & 0x1fff)] = value;
  }
  pub fn write_oam(&mut self, addr: u16, value: u8) {
    if self.mode == Mode::AccessVram || self.mode == Mode::AccessOam {
      return;
    }
    self.oam[(addr as usize & 0xff)] = value;
  }
  pub fn read_video_ram(&self, addr: u16) -> u8 {
    if self.mode == Mode::AccessVram {
      return UNDEFINED_READ;
    }
    self.vram[(addr as usize & 0x1fff)]
  }
  pub fn read_oam(&self, addr: u16) -> u8 {
    if self.mode == Mode::AccessVram || self.mode == Mode::AccessOam {
      return UNDEFINED_READ;
    }
    self.oam[(addr as usize & 0xff)]
  }
  fn switch_mode<I: CoreContext + InterruptRequest>(&mut self, mode: Mode, ctx: &mut I) {
    self.mode = mode;
    self.cycles += self.mode.cycles(self.scroll_x);
    match self.mode {
      Mode::AccessOam => {
        if self.stat.contains(Stat::ACCESS_OAM_INT) {
          ctx.request_t34_interrupt(InterruptLine::STAT);
        }
      }
      Mode::HBlank => {}
      Mode::VBlank => {
        ctx.request_t34_interrupt(InterruptLine::VBLANK);
        if self.stat.contains(Stat::VBLANK_INT) {
          ctx.request_t34_interrupt(InterruptLine::STAT);
        }
        if self.stat.contains(Stat::ACCESS_OAM_INT) {
          ctx.request_t34_interrupt(InterruptLine::STAT);
        }
      }
      _ => (),
    }
  }
  pub fn emulate<I: CoreContext + InterruptRequest>(&mut self, ctx: &mut I) {
    if !self.control.contains(Control::LCD_ON) {
      return;
    }

    self.cycles -= 1;
    if self.cycles == 1 && self.mode == Mode::AccessVram {
      // STAT mode=0 interrupt happens one cycle before the actual mode switch!
      if self.stat.contains(Stat::HBLANK_INT) {
        ctx.request_t34_interrupt(InterruptLine::STAT);
      }
    }
    if self.cycles > 0 {
      return;
    }

    match self.mode {
      Mode::AccessOam => self.switch_mode(Mode::AccessVram, ctx),
      Mode::AccessVram => {
        self.draw_line();
        self.switch_mode(Mode::HBlank, ctx)
      }
      Mode::HBlank => {
        self.current_line += 1;
        if self.current_line < 144 {
          self.switch_mode(Mode::AccessOam, ctx);
        } else {
          if let Some(callbacks) = ctx.callbacks() {
            callbacks.trigger_emu_events(EmuEvents::VSYNC);
          }
          self.switch_mode(Mode::VBlank, ctx);
        }
        self.check_compare_interrupt(ctx);
      }
      Mode::VBlank => {
        self.current_line += 1;
        if self.current_line > 153 {
          self.current_line = 0;
          self.switch_mode(Mode::AccessOam, ctx);
        } else {
          self.cycles += VBLANK_LINE_CYCLES;
        }
        self.check_compare_interrupt(ctx);
      }
    };
  }
  fn check_compare_interrupt<I: CoreContext + InterruptRequest>(&mut self, ctx: &mut I) {
    if self.current_line != self.compare_line {
      self.stat.remove(Stat::COMPARE);
    } else {
      self.stat.insert(Stat::COMPARE);
      if self.stat.contains(Stat::COMPARE_INT) {
        ctx.request_t34_interrupt(InterruptLine::STAT);
      }
    }
  }
  fn draw_line(&mut self) {
    let slice_start = gameboy::SCREEN_WIDTH * self.current_line as usize;
    let slice_end = gameboy::SCREEN_WIDTH + slice_start;
    let pixels = &mut self.back_buffer[slice_start..slice_end];
    let mut bg_prio = [false; gameboy::SCREEN_WIDTH];

    if self.control.contains(Control::BG_ON) {
      let map_mask = if self.control.contains(Control::BG_MAP) {
        0x1c00
      } else {
        0x1800
      };

      let y = self.current_line.wrapping_add(self.scroll_y);
      let row = (y / 8) as usize;
      for i in 0..gameboy::SCREEN_WIDTH {
        let x = (i as u8).wrapping_add(self.scroll_x);
        let col = (x / 8) as usize;

        let tile_num = self.vram[(((row * 32 + col) | map_mask) & 0x1fff)] as usize;
        let tile_num = if self.control.contains(Control::BG_ADDR) {
          tile_num as usize
        } else {
          128 + ((tile_num as i8 as i16) + 128) as usize
        };

        let line = ((y % 8) * 2) as usize;
        let tile_mask = tile_num << 4;
        let data1 = self.vram[(tile_mask | line) & 0x1fff];
        let data2 = self.vram[(tile_mask | (line + 1)) & 0x1fff];

        let bit = (x % 8).wrapping_sub(7).wrapping_mul(0xff) as usize;
        let color_value = (data2.bit(bit) << 1) | data1.bit(bit);
        let raw_color = Color::from_u8(color_value);
        let color = self.bg_palette.get(&raw_color);
        bg_prio[i] = raw_color != Color::Off;
        pixels[i] = color;
      }
    }
    if self.control.contains(Control::WINDOW_ON) && self.window_y <= self.current_line {
      let map_mask = if self.control.contains(Control::WINDOW_MAP) {
        0x1c00
      } else {
        0x1800
      };
      let window_x = self.window_x.wrapping_sub(7);

      let y = self.current_line - self.window_y;
      let row = (y / 8) as usize;
      for i in (window_x as usize)..gameboy::SCREEN_WIDTH {
        let mut x = (i as u8).wrapping_add(self.scroll_x);
        if x >= window_x {
          x = i as u8 - window_x;
        }
        let col = (x / 8) as usize;

        let tile_num = self.vram[(((row * 32 + col) | map_mask) & 0x1fff)] as usize;
        let tile_num = if self.control.contains(Control::BG_ADDR) {
          tile_num as usize
        } else {
          128 + ((tile_num as i8 as i16) + 128) as usize
        };

        let line = ((y % 8) * 2) as usize;
        let tile_mask = tile_num << 4;
        let data1 = self.vram[(tile_mask | line) & 0x1fff];
        let data2 = self.vram[(tile_mask | (line + 1)) & 0x1fff];

        let bit = (x % 8).wrapping_sub(7).wrapping_mul(0xff) as usize;
        let color_value = (data2.bit(bit) << 1) | data1.bit(bit);
        let raw_color = Color::from_u8(color_value);
        let color = self.bg_palette.get(&raw_color);
        bg_prio[i] = raw_color != Color::Off;
        pixels[i] = color;
      }
    }
    if self.control.contains(Control::OBJ_ON) {
      let size = if self.control.contains(Control::OBJ_SIZE) {
        16
      } else {
        8
      };

      let current_line = self.current_line;

      let mut sprites_to_draw: ArrayVec<[(usize, Sprite); 10]> = self
        .oam
        .chunks(4)
        .filter_map(|chunk| match chunk {
          &[y, x, tile_num, flags] => {
            let y = y.wrapping_sub(16);
            let x = x.wrapping_sub(8);
            let flags = SpriteFlags::from_bits_truncate(flags);
            if current_line.wrapping_sub(y) < size {
              Some(Sprite {
                y,
                x,
                tile_num,
                flags,
              })
            } else {
              None
            }
          }
          _ => None,
        })
        .take(10)
        .enumerate()
        .collect();

      sprites_to_draw.sort_by(|&(a_index, a), &(b_index, b)| {
        match a.x.cmp(&b.x) {
          // If X coordinates are the same, use OAM index as priority (low index => draw last)
          Ordering::Equal => a_index.cmp(&b_index).reverse(),
          // Use X coordinate as priority (low X => draw last)
          other => other.reverse(),
        }
      });

      for (_, sprite) in sprites_to_draw {
        let palette = if sprite.flags.contains(SpriteFlags::PALETTE) {
          &self.obj_palette1
        } else {
          &self.obj_palette0
        };
        let mut tile_num = sprite.tile_num as usize;
        let mut line = if sprite.flags.contains(SpriteFlags::FLIPY) {
          size - current_line.wrapping_sub(sprite.y) - 1
        } else {
          current_line.wrapping_sub(sprite.y)
        };
        if line >= 8 {
          tile_num += 1;
          line -= 8;
        }
        line *= 2;
        let tile_mask = tile_num << 4;
        let data1 = self.vram[(tile_mask | line as usize) & 0x1fff];
        let data2 = self.vram[(tile_mask | (line + 1) as usize) & 0x1fff];

        for x in (0..8).rev() {
          let bit = if sprite.flags.contains(SpriteFlags::FLIPX) {
            7 - x
          } else {
            x
          } as usize;
          let raw_color = Color::from_u8((data2.bit(bit) << 1) | data1.bit(bit));
          let color = palette.get(&raw_color);
          let target_x = sprite.x.wrapping_add(7 - x);
          if target_x < gameboy::SCREEN_WIDTH as u8 && raw_color != Color::Off {
            if !sprite.flags.contains(SpriteFlags::PRIORITY) || !bg_prio[target_x as usize] {
              pixels[target_x as usize] = color;
            }
          }
        }
      }
    }
  }
}

impl fmt::Debug for Ppu {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    write!(
      f,
      "LCDC:{:08b} STAT:{:08b} LY:{:02x} ",
      self.get_control(),
      self.get_stat(),
      self.get_current_line()
    )
  }
}
