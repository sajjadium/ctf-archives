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
use std::path::PathBuf;
use std::time::{Duration, Instant};

use mooneye_gb::config::{Bootrom, Cartridge, HardwareConfig, Model};
use mooneye_gb::emulation::{EmuEvents, EmuTime};
use mooneye_gb::machine::Machine;

macro_rules! resolve_model (
  (dmg0) => (Model::Dmg0);
  (dmg) => (Model::Dmg);
  (sgb) => (Model::Sgb);
  (mgb) => (Model::Mgb);
  (sgb2) => (Model::Sgb2);
);

macro_rules! testcases {
  (
    $name:ident($path:expr, $(#[$attrs:meta])* all);
    $(
      $t_name:ident($t_path:expr, $($(#[$t_attrs:meta])* $t_model:ident),*);
    )*
  ) => {
    testcases! {
      $name(
        $path,
        $(#[$attrs])* dmg0,
        $(#[$attrs])* dmg,
        $(#[$attrs])* sgb,
        $(#[$attrs])* mgb,
        $(#[$attrs])* sgb2
      );
      $(
        $t_name($t_path, $($(#[$t_attrs])* $t_model),*);
      )*
    }
  };
  (
    $name:ident($path:expr, $($(#[$attrs:meta])* $model:ident),+);
    $(
      $t_name:ident($t_path:expr, $($(#[$t_attrs:meta])* $t_model:ident),*);
    )*
  ) => {
    mod $name {
      use mooneye_gb::config::Model;
      use super::run_test_with_model;

      $(
        $(#[$attrs])*
        #[test]
        fn $model() {
          run_test_with_model($path, resolve_model!($model));
        }
       )+
    }
    $(
      testcases! {
        $t_name($t_path, $($(#[$t_attrs])* $t_model),*);
      }
    )*
  };
}

testcases! {
  add_sp_e_timing("acceptance/add_sp_e_timing", all);
  boot_div_dmg0("acceptance/boot_div-dmg0", #[ignore] dmg0);
  boot_div_dmg_abc_mgb("acceptance/boot_div-dmgABCmgb", #[ignore] dmg, #[ignore] mgb);
  boot_div_s("acceptance/boot_div-S", #[ignore] sgb, #[ignore] sgb2);
  boot_div2_s("acceptance/boot_div2-S", #[ignore] sgb, #[ignore] sgb2);
  boot_hwio_dmg0("acceptance/boot_hwio-dmg0", #[ignore] dmg0);
  boot_hwio_dmg_abc_mgb("acceptance/boot_hwio-dmgABCmgb", #[ignore] dmg, #[ignore] mgb);
  boot_hwio_s("acceptance/boot_hwio-S", sgb, sgb2);
  boot_regs_dmg0("acceptance/boot_regs-dmg0", dmg0);
  boot_regs_dmg_abc("acceptance/boot_regs-dmgABC", dmg);
  boot_regs_mgb("acceptance/boot_regs-mgb", mgb);
  boot_regs_sgb("acceptance/boot_regs-sgb", sgb);
  boot_regs_sgb2("acceptance/boot_regs-sgb2", sgb2);
  call_cc_timing("acceptance/call_cc_timing", all);
  call_cc_timing2("acceptance/call_cc_timing2", all);
  call_timing("acceptance/call_timing", all);
  call_timing2("acceptance/call_timing2", all);
  di_timing_gs("acceptance/di_timing-GS", all);
  div_timing("acceptance/div_timing", all);
  ei_sequence("acceptance/ei_sequence", all);
  ei_timing("acceptance/ei_timing", all);
  halt_ime0_ei("acceptance/halt_ime0_ei", all);
  halt_ime0_nointr_timing("acceptance/halt_ime0_nointr_timing", all);
  halt_ime1_timing("acceptance/halt_ime1_timing", all);
  halt_ime1_timing2_gs("acceptance/halt_ime1_timing2-GS", all);
  if_ie_registers("acceptance/if_ie_registers", all);
  intr_timing("acceptance/intr_timing", all);
  jp_cc_timing("acceptance/jp_cc_timing", all);
  jp_timing("acceptance/jp_timing", all);
  ld_hl_sp_e_timing("acceptance/ld_hl_sp_e_timing", all);
  oam_dma_restart("acceptance/oam_dma_restart", all);
  oam_dma_start("acceptance/oam_dma_start", all);
  oam_dma_timing("acceptance/oam_dma_timing", all);
  pop_timing("acceptance/pop_timing", all);
  push_timing("acceptance/push_timing", all);
  rapid_di_ei("acceptance/rapid_di_ei", all);
  ret_timing("acceptance/ret_timing", all);
  reti_timing("acceptance/reti_timing", all);
  ret_cc_timing("acceptance/ret_cc_timing", all);
  reti_intr_timing("acceptance/reti_intr_timing", all);
  rst_timing("acceptance/rst_timing", all);
  bits_mem_oam("acceptance/bits/mem_oam", all);
  bits_reg_f("acceptance/bits/reg_f", all);
  bits_unused_hwio_gs("acceptance/bits/unused_hwio-GS", all);
  instr_daa("acceptance/instr/daa", all);
  interrupts_ie_push("acceptance/interrupts/ie_push", all);
  oam_dma_basic("acceptance/oam_dma/basic", all);
  oam_dma_reg_read("acceptance/oam_dma/reg_read", all);
  oam_dma_sources_gs("acceptance/oam_dma/sources-GS", dmg, mgb, sgb, sgb2);
  ppu_hblank_ly_scx_timing_gs("acceptance/ppu/hblank_ly_scx_timing-GS", all);
  ppu_intr_1_2_timing_gs("acceptance/ppu/intr_1_2_timing-GS", all);
  ppu_intr_2_0_timing("acceptance/ppu/intr_2_0_timing", all);
  ppu_intr_2_mode0_timing("acceptance/ppu/intr_2_mode0_timing", all);
  ppu_stat_lyc_onoff("acceptance/ppu/stat_lyc_onoff", #[ignore] all);
  ppu_intr_2_mode0_timing_sprites("acceptance/ppu/intr_2_mode0_timing_sprites", #[ignore] all);
  ppu_intr_2_mode3_timing("acceptance/ppu/intr_2_mode3_timing", all);
  ppu_intr_2_oam_ok_timing("acceptance/ppu/intr_2_oam_ok_timing", all);
  ppu_lcdon_timing_gs("acceptance/ppu/lcdon_timing-GS", #[ignore] dmg, #[ignore] mgb, #[ignore] sgb, #[ignore] sgb2);
  ppu_lcdon_write_timing_gs("acceptance/ppu/lcdon_write_timing-GS", #[ignore] all);
  ppu_stat_irq_blocking("acceptance/ppu/stat_irq_blocking", #[ignore] all);
  ppu_vblank_stat_intr_gs("acceptance/ppu/vblank_stat_intr-GS", all);
  serial_boot_sclk_align_dmg_abc_mgb("acceptance/serial/boot_sclk_align-dmgABCmgb", #[ignore] dmg, #[ignore] mgb, #[ignore] sgb, #[ignore] sgb2);
  timer_div_write("acceptance/timer/div_write", all);
  timer_rapid_toggle("acceptance/timer/rapid_toggle", all);
  timer_tim00("acceptance/timer/tim00", all);
  timer_tim00_div_trigger("acceptance/timer/tim00_div_trigger", all);
  timer_tim01("acceptance/timer/tim01", all);
  timer_tim01_div_trigger("acceptance/timer/tim01_div_trigger", all);
  timer_tim10("acceptance/timer/tim10", all);
  timer_tim10_div_trigger("acceptance/timer/tim10_div_trigger", all);
  timer_tim11("acceptance/timer/tim11", all);
  timer_tim11_div_trigger("acceptance/timer/tim11_div_trigger", all);
  timer_tima_reload("acceptance/timer/tima_reload", all);
  timer_tima_write_reloading("acceptance/timer/tima_write_reloading", all);
  timer_tma_write_reloading("acceptance/timer/tma_write_reloading", all);
  mbc1_bits_ramg("emulator-only/mbc1/bits_ramg", all);
  mbc1_bits_bank1("emulator-only/mbc1/bits_bank1", all);
  mbc1_bits_bank2("emulator-only/mbc1/bits_bank2", all);
  mbc1_bits_mode("emulator-only/mbc1/bits_mode", all);
  mbc1_rom_512kb("emulator-only/mbc1/rom_512kb", all);
  mbc1_rom_1mb("emulator-only/mbc1/rom_1Mb", all);
  mbc1_rom_2mb("emulator-only/mbc1/rom_2Mb", all);
  mbc1_rom_4mb("emulator-only/mbc1/rom_4Mb", all);
  mbc1_rom_8mb("emulator-only/mbc1/rom_8Mb", all);
  mbc1_rom_16mb("emulator-only/mbc1/rom_16Mb", all);
  mbc1_ram_64kb("emulator-only/mbc1/ram_64kb", all);
  mbc1_ram_25kb("emulator-only/mbc1/ram_256kb", all);
  mbc1_multicart_rom_8mb("emulator-only/mbc1/multicart_rom_8Mb", all);
  mbc2_bits_ramg("emulator-only/mbc2/bits_ramg", all);
  mbc2_bits_romb("emulator-only/mbc2/bits_romb", all);
  mbc2_bits_unused("emulator-only/mbc2/bits_unused", all);
  mbc2_rom_512kb("emulator-only/mbc2/rom_512kb", all);
  mbc2_rom_1mb("emulator-only/mbc2/rom_1Mb", all);
  mbc2_rom_2mb("emulator-only/mbc2/rom_2Mb", all);
  mbc2_ram("emulator-only/mbc2/ram", all);
  mbc5_rom_512kb("emulator-only/mbc5/rom_512kb", all);
  mbc5_rom_1mb("emulator-only/mbc5/rom_1Mb", all);
  mbc5_rom_2mb("emulator-only/mbc5/rom_2Mb", all);
  mbc5_rom_4mb("emulator-only/mbc5/rom_4Mb", all);
  mbc5_rom_8mb("emulator-only/mbc5/rom_8Mb", all);
  mbc5_rom_16mb("emulator-only/mbc5/rom_16Mb", all);
  mbc5_rom_32mb("emulator-only/mbc5/rom_32Mb", all);
  mbc5_rom_64mb("emulator-only/mbc5/rom_64Mb", all);
}

fn run_test_with_model(name: &str, model: Model) {
  let bootrom =
    Bootrom::lookup(&[model]).unwrap_or_else(|| panic!("No boot ROM found ({:?})", model));

  let test_name = format!("../tests/build/{}.gb", name);
  let cartridge_path = PathBuf::from(&test_name);
  let cartridge = Cartridge::from_path(&cartridge_path).unwrap();

  let hardware_config = HardwareConfig {
    model,
    bootrom: Some(bootrom.data),
    cartridge,
  };

  let max_duration = Duration::from_secs(120);
  let start_time = Instant::now();
  let pulse_duration = EmuTime::from_machine_cycles(1_000_000);

  let mut machine = Machine::new(hardware_config);
  let mut registers = None;
  let mut emu_time = EmuTime::zero();
  loop {
    let time = Instant::now();
    if time - start_time > max_duration {
      break;
    }
    let (events, end_time) = machine.emulate(emu_time + pulse_duration);
    emu_time = end_time;
    if events.contains(EmuEvents::DEBUG_OP) {
      registers = Some(machine.regs());
      break;
    }
  }
  match registers {
    None => panic!("Test did not finish ({:?})", model),
    Some(regs) => {
      if regs.a != 0 {
        panic!(
          "{} assertion failures in hardware test ({:?})",
          regs.a, model
        );
      }
      if regs.b != 3 || regs.c != 5 || regs.d != 8 || regs.e != 13 || regs.h != 21 || regs.l != 34 {
        panic!("Hardware test failed ({:?})", model);
      }
    }
  }
}
