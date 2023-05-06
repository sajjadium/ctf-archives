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
use crate::cpu::decode::{Cond, In8, Out8};
use crate::cpu::register_file::Reg16;
use crate::cpu::{Cpu, CpuContext, Step};
use crate::util::int::IntExt;

impl Cpu {
  // --- 8-bit operations
  // 8-bit loads
  /// LD d, s
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn load<B: CpuContext, O: Copy, I: Copy>(&mut self, ctx: &mut B, out8: O, in8: I) -> Step
  where
    Self: Out8<O> + In8<I>,
  {
    let value = self.read(in8, ctx);
    self.write(out8, ctx, value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  // Magic breakpoint
  pub fn ld_b_b<B>(&mut self, ctx: &mut B) -> Step
  where
    B: CpuContext,
  {
    if let Some(callbacks) = ctx.callbacks() {
      callbacks.debug_opcode();
    }
    self.prefetch_next(ctx, self.regs.pc)
  }
  // 8-bit arithmetic
  /// ADD s
  ///
  /// Flags: Z N H C
  ///        * 0 * *
  pub fn add<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx);
    let (result, carry) = self.regs.a.overflowing_add(value);
    let half_carry = (self.regs.a & 0x0f).checked_add(value | 0xf0).is_none();
    self.regs.set_zf(result == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(half_carry);
    self.regs.set_cf(carry);
    self.regs.a = result;
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// ADC s
  ///
  /// Flags: Z N H C
  ///        * 0 * *
  pub fn adc<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx);
    let cy = self.regs.cf() as u8;
    let result = self.regs.a.wrapping_add(value).wrapping_add(cy);
    self.regs.set_zf(result == 0);
    self.regs.set_nf(false);
    self
      .regs
      .set_hf((self.regs.a & 0xf) + (value & 0xf) + cy > 0xf);
    self
      .regs
      .set_cf(self.regs.a as u16 + value as u16 + cy as u16 > 0xff);
    self.regs.a = result;
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// SUB s
  ///
  /// Flags: Z N H C
  ///        * 1 * *
  pub fn sub<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx);
    self.regs.a = self.alu_sub(value, false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// SBC s
  ///
  /// Flags: Z N H C
  ///        * 1 * *
  pub fn sbc<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx);
    self.regs.a = self.alu_sub(value, self.regs.cf());
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// CP s
  ///
  /// Flags: Z N H C
  ///        * 1 * *
  pub fn cp<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx);
    self.alu_sub(value, false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// AND s
  ///
  /// Flags: Z N H C
  ///        * 0 1 0
  pub fn and<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx);
    self.regs.a &= value;
    self.regs.set_zf(self.regs.a == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(true);
    self.regs.set_cf(false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// OR s
  ///
  /// Flags: Z N H C
  ///        * 0 0 0
  pub fn or<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx);
    self.regs.a |= value;
    self.regs.set_zf(self.regs.a == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// XOR s
  ///
  /// Flags: Z N H C
  ///        * 0 0 0
  pub fn xor<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx);
    self.regs.a ^= value;
    self.regs.set_zf(self.regs.a == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// INC s
  ///
  /// Flags: Z N H C
  ///        * 0 * -
  pub fn inc<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: In8<IO> + Out8<IO>,
  {
    let value = self.read(io, ctx);
    let new_value = value.wrapping_add(1);
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(value & 0xf == 0xf);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// DEC s
  ///
  /// Flags: Z N H C
  ///        * 1 * -
  pub fn dec<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: In8<IO> + Out8<IO>,
  {
    let value = self.read(io, ctx);
    let new_value = value.wrapping_sub(1);
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(true);
    self.regs.set_hf(value & 0xf == 0);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RLCA
  ///
  /// Flags: Z N H C
  ///        0 0 0 *
  pub fn rlca<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let value = self.regs.a;
    self.regs.a = self.alu_rlc(value);
    self.regs.set_zf(false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RLA
  ///
  /// Flags: Z N H C
  ///        0 0 0 *
  pub fn rla<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let value = self.regs.a;
    self.regs.a = self.alu_rl(value);
    self.regs.set_zf(false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RRCA
  ///
  /// Flags: Z N H C
  ///        0 0 0 *
  pub fn rrca<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let value = self.regs.a;
    self.regs.a = self.alu_rrc(value);
    self.regs.set_zf(false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RRA
  ///
  /// Flags: Z N H C
  ///        0 0 0 *
  pub fn rra<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let value = self.regs.a;
    self.regs.a = self.alu_rr(value);
    self.regs.set_zf(false);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RLC s
  ///
  /// Flags: Z N H C
  ///        * 0 0 *
  pub fn rlc<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx);
    let new_value = self.alu_rlc(value);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RL s
  ///
  /// Flags: Z N H C
  ///        * 0 0 *
  pub fn rl<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx);
    let new_value = self.alu_rl(value);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RRC s
  ///
  /// Flags: Z N H C
  ///        * 0 0 *
  pub fn rrc<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx);
    let new_value = self.alu_rrc(value);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RR s
  ///
  /// Flags: Z N H C
  ///        * 0 0 *
  pub fn rr<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx);
    let new_value = self.alu_rr(value);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// SLA s
  ///
  /// Flags: Z N H C
  ///        * 0 0 *
  pub fn sla<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx);
    let co = value & 0x80;
    let new_value = value << 1;
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(co != 0);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// SRA s
  ///
  /// Flags: Z N H C
  ///        * 0 0 *
  pub fn sra<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx);
    let co = value & 0x01;
    let hi = value & 0x80;
    let new_value = (value >> 1) | hi;
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(co != 0);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// SRL s
  ///
  /// Flags: Z N H C
  ///        * 0 0 *
  pub fn srl<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx);
    let co = value & 0x01;
    let new_value = value >> 1;
    self.regs.set_zf(new_value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(co != 0);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// SWAP s
  ///
  /// Flags: Z N H C
  ///        * 0 0 0
  pub fn swap<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx);
    let new_value = (value >> 4) | (value << 4);
    self.regs.set_zf(value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(false);
    self.write(io, ctx, new_value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// BIT b, s
  ///
  /// Flags: Z N H C
  ///        * 0 1 -
  pub fn bit<B: CpuContext, I: Copy>(&mut self, ctx: &mut B, bit: usize, in8: I) -> Step
  where
    Self: In8<I>,
  {
    let value = self.read(in8, ctx) & (1 << bit);
    self.regs.set_zf(value == 0);
    self.regs.set_nf(false);
    self.regs.set_hf(true);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// SET b, s
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn set<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, bit: usize, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx) | (1 << bit);
    self.write(io, ctx, value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RES b, s
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn res<B: CpuContext, IO: Copy>(&mut self, ctx: &mut B, bit: usize, io: IO) -> Step
  where
    Self: Out8<IO> + In8<IO>,
  {
    let value = self.read(io, ctx) & !(1 << bit);
    self.write(io, ctx, value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  // --- Control
  /// JP nn
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn jp<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let addr = self.fetch_imm16(ctx);
    self.ctrl_jp(ctx, addr);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// JP HL
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn jp_hl<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.prefetch_next(ctx, self.regs.read16(Reg16::HL))
  }
  /// JR e
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn jr<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let offset = self.fetch_imm8(ctx) as i8;
    self.ctrl_jr(ctx, offset);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// CALL nn
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn call<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let addr = self.fetch_imm16(ctx);
    self.ctrl_call(ctx, addr);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RET
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn ret<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.ctrl_ret(ctx);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RETI
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn reti<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.ime = true;
    self.ctrl_ret(ctx);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// JP cc, nn
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn jp_cc<B: CpuContext>(&mut self, ctx: &mut B, cond: Cond) -> Step {
    let addr = self.fetch_imm16(ctx);
    if self.check_cond(cond) {
      self.ctrl_jp(ctx, addr);
    }
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// JR cc, e
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn jr_cc<B: CpuContext>(&mut self, ctx: &mut B, cond: Cond) -> Step {
    let offset = self.fetch_imm8(ctx) as i8;
    if self.check_cond(cond) {
      self.ctrl_jr(ctx, offset);
    }
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// CALL cc, nn
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn call_cc<B: CpuContext>(&mut self, ctx: &mut B, cond: Cond) -> Step {
    let addr = self.fetch_imm16(ctx);
    if self.check_cond(cond) {
      self.ctrl_call(ctx, addr);
    }
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RET cc
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn ret_cc<B: CpuContext>(&mut self, ctx: &mut B, cond: Cond) -> Step {
    ctx.tick_cycle();
    if self.check_cond(cond) {
      self.ctrl_ret(ctx);
    }
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// RST n
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn rst<B: CpuContext>(&mut self, ctx: &mut B, addr: u8) -> Step {
    let pc = self.regs.pc;
    self.push_u16(ctx, pc);
    self.prefetch_next(ctx, addr as u16)
  }
  // --- Miscellaneous
  /// HALT
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn halt<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let (interrupts, opcode) = ctx.read_cycle_intr(self.regs.pc);
    self.opcode = opcode;
    if !interrupts.is_empty() {
      if self.ime {
        Step::InterruptDispatch
      } else {
        self.decode_exec_fetch(ctx)
      }
    } else {
      ctx.tick_cycle();
      Step::Halt
    }
  }

  /// STOP
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn stop<B: CpuContext>(&mut self, _: &mut B) -> Step {
    panic!("STOP")
  }
  /// DI
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn di<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.ime = false;
    self.opcode = self.fetch_imm8(ctx);
    Step::Running
  }
  /// EI
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn ei<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let step = self.prefetch_next(ctx, self.regs.pc);
    self.ime = true;
    step
  }
  /// CCF
  ///
  /// Flags: Z N H C
  ///        - 0 0 *
  pub fn ccf<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(!self.regs.cf());
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// SCF
  ///
  /// Flags: Z N H C
  ///        - 0 0 1
  pub fn scf<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.regs.set_nf(false);
    self.regs.set_hf(false);
    self.regs.set_cf(true);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// NOP
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn nop<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// DAA
  ///
  /// Flags: Z N H C
  ///        * - 0 *
  pub fn daa<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    // DAA table in page 110 of the official "Game Boy Programming Manual"
    let mut carry = false;
    if !self.regs.nf() {
      if self.regs.cf() || self.regs.a > 0x99 {
        self.regs.a = self.regs.a.wrapping_add(0x60);
        carry = true;
      }
      if self.regs.hf() || self.regs.a & 0x0f > 0x09 {
        self.regs.a = self.regs.a.wrapping_add(0x06);
      }
    } else if self.regs.cf() {
      carry = true;
      self.regs.a = self
        .regs
        .a
        .wrapping_add(if self.regs.hf() { 0x9a } else { 0xa0 });
    } else if self.regs.hf() {
      self.regs.a = self.regs.a.wrapping_add(0xfa);
    }

    self.regs.set_zf(self.regs.a == 0);
    self.regs.set_hf(false);
    self.regs.set_cf(carry);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// CPL
  ///
  /// Flags: Z N H C
  ///        - 1 1 -
  pub fn cpl<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.regs.a = !self.regs.a;
    self.regs.set_nf(true);
    self.regs.set_hf(true);
    self.prefetch_next(ctx, self.regs.pc)
  }
  // --- 16-bit operations
  // 16-bit loads
  /// LD dd, nn
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn load16_imm<B: CpuContext>(&mut self, ctx: &mut B, reg: Reg16) -> Step {
    let value = self.fetch_imm16(ctx);
    self.regs.write16(reg, value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// LD (nn), SP
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn load16_nn_sp<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let value = self.regs.sp;
    let addr = self.fetch_imm16(ctx);
    ctx.write_cycle(addr, value as u8);
    ctx.write_cycle(addr.wrapping_add(1), (value >> 8) as u8);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// LD SP, HL
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn load16_sp_hl<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let value = self.regs.read16(Reg16::HL);
    self.regs.sp = value;
    ctx.tick_cycle();
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// LD HL, SP+e
  ///
  /// Flags: Z N H C
  ///        0 0 * *
  pub fn load16_hl_sp_e<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let offset = self.fetch_imm8(ctx) as i8 as u16;
    let sp = self.regs.sp as u16;
    let value = sp.wrapping_add(offset);
    self.regs.write16(Reg16::HL, value);
    self.regs.set_zf(false);
    self.regs.set_nf(false);
    self.regs.set_hf(u16::test_add_carry_bit(3, sp, offset));
    self.regs.set_cf(u16::test_add_carry_bit(7, sp, offset));
    ctx.tick_cycle();
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// PUSH rr
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn push16<B: CpuContext>(&mut self, ctx: &mut B, reg: Reg16) -> Step {
    let value = self.regs.read16(reg);
    self.push_u16(ctx, value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// POP rr
  ///
  /// Flags: Z N H C
  ///        - - - -
  /// Note! POP AF affects all flags
  pub fn pop16<B: CpuContext>(&mut self, ctx: &mut B, reg: Reg16) -> Step {
    let value = self.pop_u16(ctx);
    self.regs.write16(reg, value);
    self.prefetch_next(ctx, self.regs.pc)
  }
  // 16-bit arithmetic
  /// ADD HL, ss
  ///
  /// Flags: Z N H C
  ///        - 0 * *
  pub fn add16<B: CpuContext>(&mut self, ctx: &mut B, reg: Reg16) -> Step {
    let hl = self.regs.read16(Reg16::HL);
    let value = self.regs.read16(reg);
    let result = hl.wrapping_add(value);
    self.regs.set_nf(false);
    self.regs.set_hf(u16::test_add_carry_bit(11, hl, value));
    self.regs.set_cf(hl > 0xffff - value);
    self.regs.write16(Reg16::HL, result);
    ctx.tick_cycle();
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// ADD SP, e
  ///
  /// Flags: Z N H C
  ///        0 0 * *
  pub fn add16_sp_e<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    let offset = self.fetch_imm8(ctx) as i8 as i16 as u16;
    let sp = self.regs.sp;
    self.regs.sp = sp.wrapping_add(offset);
    self.regs.set_zf(false);
    self.regs.set_nf(false);
    self.regs.set_hf(u16::test_add_carry_bit(3, sp, offset));
    self.regs.set_cf(u16::test_add_carry_bit(7, sp, offset));
    ctx.tick_cycle();
    ctx.tick_cycle();
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// INC rr
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn inc16<B: CpuContext>(&mut self, ctx: &mut B, reg: Reg16) -> Step {
    let value = self.regs.read16(reg).wrapping_add(1);
    self.regs.write16(reg, value);
    ctx.tick_cycle();
    self.prefetch_next(ctx, self.regs.pc)
  }
  /// DEC rr
  ///
  /// Flags: Z N H C
  ///        - - - -
  pub fn dec16<B: CpuContext>(&mut self, ctx: &mut B, reg: Reg16) -> Step {
    let value = self.regs.read16(reg).wrapping_sub(1);
    self.regs.write16(reg, value);
    ctx.tick_cycle();
    self.prefetch_next(ctx, self.regs.pc)
  }
  // --- Undefined
  pub fn undefined<B: CpuContext>(&mut self, _: &mut B) -> Step {
    panic!("Undefined opcode {}", self.opcode)
  }
  pub fn cb_prefix<B: CpuContext>(&mut self, ctx: &mut B) -> Step {
    self.opcode = self.fetch_imm8(ctx);
    self.cb_decode_exec_fetch(ctx)
  }
}
