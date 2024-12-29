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
use std::fmt;

use crate::cpu::decode::{Addr, Cond, Immediate8, In8, Out8};
use crate::cpu::register_file::{Reg16, Reg8, RegisterFile};
use crate::hardware::interrupts::InterruptLine;
use crate::CoreContext;

mod decode;
mod execute;
pub mod register_file;

#[cfg(all(test, not(feature = "acceptance_tests")))]
mod test;

pub trait CpuContext: CoreContext {
  fn read_cycle(&mut self, addr: u16) -> u8;
  fn read_cycle_high(&mut self, addr: u8) -> u8 {
    self.read_cycle(0xff00 | (addr as u16))
  }
  fn read_cycle_intr(&mut self, addr: u16) -> (InterruptLine, u8);
  fn write_cycle(&mut self, addr: u16, data: u8);
  fn write_cycle_high(&mut self, addr: u8, data: u8) {
    self.write_cycle(0xff00 | (addr as u16), data);
  }
  fn write_cycle_intr(&mut self, addr: u16, data: u8) -> InterruptLine;
  fn tick_cycle(&mut self);
  fn has_interrupt(&self) -> bool;
  fn ack_interrupt(&mut self, mask: InterruptLine);
}

#[derive(Clone)]
pub struct Cpu {
  pub regs: RegisterFile,
  pub ime: bool,
  pub opcode: u8,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Step {
  Running,
  Halt,
  InterruptDispatch,
}

impl fmt::Display for Cpu {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    write!(f, "{}", self.regs)
  }
}
impl Cpu {
  pub fn new() -> Cpu {
    Cpu {
      regs: RegisterFile::new(),
      ime: false,
      opcode: 0x00,
    }
  }

  fn prefetch_next<H: CpuContext>(&mut self, ctx: &mut H, addr: u16) -> Step {
    let (interrupts, opcode) = ctx.read_cycle_intr(addr);
    self.opcode = opcode;
    if self.ime && !interrupts.is_empty() {
      Step::InterruptDispatch
    } else {
      self.regs.pc = addr.wrapping_add(1);
      Step::Running
    }
  }

  fn fetch_imm8<H: CpuContext>(&mut self, ctx: &mut H) -> u8 {
    let addr = self.regs.pc;
    self.regs.pc = self.regs.pc.wrapping_add(1);
    ctx.read_cycle(addr)
  }
  fn fetch_imm16<H: CpuContext>(&mut self, ctx: &mut H) -> u16 {
    let lo = self.fetch_imm8(ctx);
    let hi = self.fetch_imm8(ctx);
    u16::from_le_bytes([lo, hi])
  }

  fn pop_u16<H: CpuContext>(&mut self, ctx: &mut H) -> u16 {
    let lo = ctx.read_cycle(self.regs.sp);
    self.regs.sp = self.regs.sp.wrapping_add(1);
    let hi = ctx.read_cycle(self.regs.sp);
    self.regs.sp = self.regs.sp.wrapping_add(1);
    u16::from_le_bytes([lo, hi])
  }
  fn push_u16<H: CpuContext>(&mut self, ctx: &mut H, value: u16) {
    let [lo, hi] = u16::to_le_bytes(value);
    ctx.tick_cycle();
    self.regs.sp = self.regs.sp.wrapping_sub(1);
    ctx.write_cycle(self.regs.sp, hi);
    self.regs.sp = self.regs.sp.wrapping_sub(1);
    ctx.write_cycle(self.regs.sp, lo);
  }

  fn check_cond(&self, cond: Cond) -> bool {
    match cond {
      Cond::NZ => !self.regs.zf(),
      Cond::Z => self.regs.zf(),
      Cond::NC => !self.regs.cf(),
      Cond::C => self.regs.cf(),
    }
  }

  pub fn execute_step<H: CpuContext>(&mut self, ctx: &mut H, step: Step) -> Step {
    match step {
      Step::Running => self.decode_exec_fetch(ctx),
      Step::InterruptDispatch => {
        self.ime = false;
        ctx.tick_cycle();

        let [lo, hi] = u16::to_le_bytes(self.regs.pc);
        ctx.tick_cycle();

        self.regs.sp = self.regs.sp.wrapping_sub(1);
        ctx.write_cycle(self.regs.sp, hi);

        self.regs.sp = self.regs.sp.wrapping_sub(1);
        let interrupts = ctx.write_cycle_intr(self.regs.sp, lo);

        let interrupt = interrupts.highest_priority();
        ctx.ack_interrupt(interrupt);
        self.regs.pc = match interrupt {
          InterruptLine::VBLANK => 0x0040,
          InterruptLine::STAT => 0x0048,
          InterruptLine::TIMER => 0x0050,
          InterruptLine::SERIAL => 0x0058,
          InterruptLine::JOYPAD => 0x0060,
          _ => 0x0000,
        };
        self.opcode = self.fetch_imm8(ctx);
        Step::Running
      }
      Step::Halt => {
        if ctx.has_interrupt() {
          self.prefetch_next(ctx, self.regs.pc)
        } else {
          ctx.tick_cycle();
          Step::Halt
        }
      }
    }
  }

  fn alu_sub(&mut self, value: u8, carry: bool) -> u8 {
    let cy = carry as u8;
    let result = self.regs.a.wrapping_sub(value).wrapping_sub(cy);
    self.regs.set_zf(result == 0);
    self.regs.set_nf(true);
    self.regs.set_hf(
      (self.regs.a & 0xf)
        .wrapping_sub(value & 0xf)
        .wrapping_sub(cy)
        & (0xf + 1)
        != 0,
    );
    self
      .regs
      .set_cf((self.regs.a as u16) < (value as u16) + (cy as u16));
    result
  }
  fn alu_rl(&mut self, value: u8) -> u8 {
    let ci = self.regs.cf() as u8;
    let co = value & 0x80;
    let new_value = (value << 1) | ci;
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(co != 0);
    new_value
  }
  fn alu_rlc(&mut self, value: u8) -> u8 {
    let co = value & 0x80;
    let new_value = value.rotate_left(1);
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(co != 0);
    new_value
  }
  fn alu_rr(&mut self, value: u8) -> u8 {
    let ci = self.regs.cf() as u8;
    let co = value & 0x01;
    let new_value = (value >> 1) | (ci << 7);
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(co != 0);
    new_value
  }
  fn alu_rrc(&mut self, value: u8) -> u8 {
    let co = value & 0x01;
    let new_value = value.rotate_right(1);
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(co != 0);
    new_value
  }
  fn ctrl_jp<H: CpuContext>(&mut self, ctx: &mut H, addr: u16) {
    self.regs.pc = addr;
    ctx.tick_cycle();
  }
  fn ctrl_jr<H: CpuContext>(&mut self, ctx: &mut H, offset: i8) {
    self.regs.pc = self.regs.pc.wrapping_add(offset as u16);
    ctx.tick_cycle();
  }
  fn ctrl_call<H: CpuContext>(&mut self, ctx: &mut H, addr: u16) {
    self.push_u16(ctx, self.regs.pc);
    self.regs.pc = addr;
  }
  fn ctrl_ret<H: CpuContext>(&mut self, ctx: &mut H) {
    self.regs.pc = self.pop_u16(ctx);
    ctx.tick_cycle();
  }
}

impl In8<Reg8> for Cpu {
  fn read<H: CpuContext>(&mut self, src: Reg8, _: &mut H) -> u8 {
    use self::register_file::Reg8::*;
    match src {
      A => self.regs.a,
      B => self.regs.b,
      C => self.regs.c,
      D => self.regs.d,
      E => self.regs.e,
      H => self.regs.h,
      L => self.regs.l,
    }
  }
}
impl Out8<Reg8> for Cpu {
  fn write<H: CpuContext>(&mut self, dst: Reg8, _: &mut H, data: u8) {
    use self::register_file::Reg8::*;
    match dst {
      A => self.regs.a = data,
      B => self.regs.b = data,
      C => self.regs.c = data,
      D => self.regs.d = data,
      E => self.regs.e = data,
      H => self.regs.h = data,
      L => self.regs.l = data,
    }
  }
}
impl In8<Immediate8> for Cpu {
  fn read<H: CpuContext>(&mut self, _: Immediate8, ctx: &mut H) -> u8 {
    self.fetch_imm8(ctx)
  }
}
impl In8<Addr> for Cpu {
  fn read<H: CpuContext>(&mut self, src: Addr, ctx: &mut H) -> u8 {
    use crate::cpu::decode::Addr::*;
    match src {
      BC => {
        let addr = self.regs.read16(Reg16::BC);
        ctx.read_cycle(addr)
      }
      DE => {
        let addr = self.regs.read16(Reg16::DE);
        ctx.read_cycle(addr)
      }
      HL => {
        let addr = self.regs.read16(Reg16::HL);
        ctx.read_cycle(addr)
      }
      HLD => {
        let addr = self.regs.read16(Reg16::HL);
        self.regs.write16(Reg16::HL, addr.wrapping_sub(1));
        ctx.read_cycle(addr)
      }
      HLI => {
        let addr = self.regs.read16(Reg16::HL);
        self.regs.write16(Reg16::HL, addr.wrapping_add(1));
        ctx.read_cycle(addr)
      }
      Direct => {
        let addr = self.fetch_imm16(ctx);
        ctx.read_cycle(addr)
      }
      ZeroPage => {
        let addr = self.fetch_imm8(ctx);
        ctx.read_cycle_high(addr)
      }
      ZeroPageC => ctx.read_cycle_high(self.regs.c),
    }
  }
}
impl Out8<Addr> for Cpu {
  fn write<H: CpuContext>(&mut self, dst: Addr, ctx: &mut H, data: u8) {
    use crate::cpu::decode::Addr::*;
    match dst {
      BC => {
        let addr = self.regs.read16(Reg16::BC);
        ctx.write_cycle(addr, data)
      }
      DE => {
        let addr = self.regs.read16(Reg16::DE);
        ctx.write_cycle(addr, data)
      }
      HL => {
        let addr = self.regs.read16(Reg16::HL);
        ctx.write_cycle(addr, data)
      }
      HLD => {
        let addr = self.regs.read16(Reg16::HL);
        self.regs.write16(Reg16::HL, addr.wrapping_sub(1));
        ctx.write_cycle(addr, data)
      }
      HLI => {
        let addr = self.regs.read16(Reg16::HL);
        self.regs.write16(Reg16::HL, addr.wrapping_add(1));
        ctx.write_cycle(addr, data)
      }
      Direct => {
        let addr = self.fetch_imm16(ctx);
        ctx.write_cycle(addr, data)
      }
      ZeroPage => {
        let addr = self.fetch_imm8(ctx);
        ctx.write_cycle_high(addr, data)
      }
      ZeroPageC => ctx.write_cycle_high(self.regs.c, data),
    }
  }
}
