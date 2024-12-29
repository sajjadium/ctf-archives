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
use glium::glutin;
use mooneye_gb::{
    config::HardwareConfig,
    emulation::{EmuEvents, EmuTime},
    hardware::Hardware,
    machine::Machine,
    *,
};
use std::time::Duration;

use crate::{renderer::Renderer, replay::ReplayMode, GB_KEYS};

pub struct State {
    pub machine: Machine,
    pub delta: Duration,
    pub emu_time: EmuTime,
    pub last_keys: [bool; GB_KEYS],
    pub keys: [bool; GB_KEYS],
    pub replay_mode: ReplayMode,
    pub ticks_until_flag: Option<usize>,
}

impl State {
    pub fn from_config(config: HardwareConfig, replay_mode: ReplayMode) -> State {
        let machine = Machine::new(config);
        State {
            emu_time: machine.emu_time(),
            machine,
            delta: Duration::default(),
            last_keys: [false; GB_KEYS],
            keys: [false; GB_KEYS],
            replay_mode,
            ticks_until_flag: None,
        }
    }

    // Returns false if replay playback ended
    #[must_use]
    pub fn tick<R: Renderer>(&mut self, renderer: &mut R) -> bool {
        let current_tick = match &mut self.replay_mode {
            ReplayMode::Playback { keys_log, current } => {
                if *current >= keys_log.len() {
                    return false;
                }

                self.keys = keys_log[*current];
                *current += 1;
                *current
            }
            ReplayMode::Record { keys_log, .. } => {
                keys_log.push(self.keys);
                keys_log.len()
            }
        };

        for i in 0..GB_KEYS {
            if self.keys[i] != self.last_keys[i] {
                let key = GbKey::from_num(i);
                match self.keys[i] {
                    true => self.machine.key_down(key),
                    false => self.machine.key_up(key),
                }
            }
        }

        let machine_cycles =
            EmuTime::from_machine_cycles(((self.delta * CPU_SPEED_HZ as u32).as_secs() as u64) / 4);

        let target_time = self.emu_time + machine_cycles;
        loop {
            let (events, end_time) = self.machine.emulate(target_time);

            if events.contains(EmuEvents::VSYNC) {
                if self.ticks_until_flag.is_none() && flag_is_found(self.machine.hardware()) {
                    // self.ticks_until_flag = Some(current_tick)
                    // Read out baba's steps from memory
                    // Don't use the higher-level Hardware.read() function since we don't want to
                    // emulate a memory cycle
                    let mut steps:u16 = (self
                        .machine
                        .hardware()
                        .peripherals
                        .work_ram
                        .read_lower(0xc3a5) as u16) << 8;
                    steps += self
                        .machine
                        .hardware()
                        .peripherals
                        .work_ram
                        .read_lower(0xc3a4) as u16;
                    self.ticks_until_flag = Some(steps as usize);
                }
                renderer.update_pixels(self.machine.screen_buffer());
            }

            if end_time >= target_time {
                self.emu_time = end_time;
                break;
            }
        }
        self.last_keys = self.keys;

        true
    }

    pub fn handle_keyboard(&mut self, input: glutin::event::KeyboardInput) {
        use glutin::event::ElementState;
        if let Some(keycode) = input.virtual_keycode {
            if let Some(key) = map_keycode(keycode) {
                match input.state {
                    ElementState::Pressed => self.keys[key.to_num()] = true,
                    ElementState::Released => self.keys[key.to_num()] = false,
                }
            }
        }
    }
}

fn flag_is_found(hardware: &Hardware) -> bool {
    hardware.peripherals.work_ram.read_lower(0xc3a2) == 0x10
}

fn map_keycode(key: glutin::event::VirtualKeyCode) -> Option<GbKey> {
    use glium::glutin::event::VirtualKeyCode::*;
    match key {
        Right => Some(GbKey::Right),
        Left => Some(GbKey::Left),
        Up => Some(GbKey::Up),
        Down => Some(GbKey::Down),
        Z => Some(GbKey::A),
        X => Some(GbKey::B),
        Return => Some(GbKey::Start),
        Back => Some(GbKey::Select),
        _ => None,
    }
}

trait GbKeyNum {
    fn to_num(&self) -> usize;
    fn from_num(num: usize) -> Self;
}

impl GbKeyNum for GbKey {
    fn to_num(&self) -> usize {
        match self {
            GbKey::Right => 0,
            GbKey::Left => 1,
            GbKey::Up => 2,
            GbKey::Down => 3,
            GbKey::A => 4,
            GbKey::B => 5,
            GbKey::Start => 6,
            GbKey::Select => 7,
        }
    }

    fn from_num(num: usize) -> GbKey {
        match num {
            0 => GbKey::Right,
            1 => GbKey::Left,
            2 => GbKey::Up,
            3 => GbKey::Down,
            4 => GbKey::A,
            5 => GbKey::B,
            6 => GbKey::Start,
            7 => GbKey::Select,
            n => panic!("invalid num {} for key", n),
        }
    }
}
