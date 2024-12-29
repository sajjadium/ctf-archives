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
use anyhow::{anyhow, Error};
use gilrs::{Axis, Button, EventType, Gilrs};
use glium::glutin::dpi::LogicalSize;
use glium::glutin::event::{Event, WindowEvent};
use glium::glutin::event_loop::{ControlFlow, EventLoop};
use glium::{glutin, Api, Display, Surface, Version};
use imgui_winit_support::HiDpiMode;
use log::{error, info};
use mooneye_gb::config::{Bootrom, Cartridge, HardwareConfig};
use mooneye_gb::emulation::{EmuEvents, EmuTime};
use mooneye_gb::machine::Machine;
use mooneye_gb::*;
use std::path::Path;
use std::time::Duration;

use crate::fps_counter::FpsCounter;
use crate::frame_times::FrameTimes;
use crate::frontend::gui::Screen;
use crate::frontend::renderer::Renderer;
use crate::perf_counter::PerfCounter;

mod gui;
mod renderer;

enum FrontendState {
  WaitBootrom(Option<Cartridge>, gui::WaitBootromScreen),
  InGame(InGameState),
}

impl FrontendState {
  pub fn update_delta_time(&mut self, delta: Duration) {
    if let FrontendState::InGame(state) = self {
      state.update_delta_time(delta);
    }
  }
  pub fn handle_gilrs(&mut self, event: gilrs::EventType) {
    if let FrontendState::InGame(InGameState { machine, .. }) = self {
      match event {
        EventType::ButtonPressed(button, _) => {
          if let Some(key) = map_button(button) {
            machine.key_down(key);
          }
        }
        EventType::ButtonReleased(button, _) => {
          if let Some(key) = map_button(button) {
            machine.key_up(key);
          }
        }
        EventType::AxisChanged(axis, value, _) => {
          if let Some((key, state)) = map_axis(axis, value) {
            if state {
              machine.key_down(key);
            } else {
              machine.key_up(key);
            }
          }
        }
        _ => (),
      }
    }
  }
  pub fn handle_keyboard(&mut self, input: glutin::event::KeyboardInput) {
    use glium::glutin::event::{ElementState, VirtualKeyCode};
    if let FrontendState::InGame(InGameState {
      machine, screen, ..
    }) = self
    {
      if let Some(keycode) = input.virtual_keycode {
        if let Some(key) = map_keycode(keycode) {
          match input.state {
            ElementState::Pressed => machine.key_down(key),
            ElementState::Released => machine.key_up(key),
          }
        }
        match (keycode, input.state) {
          (VirtualKeyCode::F2, ElementState::Pressed) => screen.toggle_info_overlay(),
          _ => (),
        }
      }
    }
  }
  pub fn tick(&mut self, renderer: &mut Renderer, ui: &imgui::Ui) {
    match self {
      FrontendState::WaitBootrom(_, screen) => screen.render(ui),
      FrontendState::InGame(state) => {
        state.tick(renderer, ui);
      }
    }
  }
  pub fn drop_file(&mut self, path: &Path) {
    match self {
      FrontendState::WaitBootrom(cartridge, screen) => match Bootrom::from_path(&path) {
        Ok(bootrom) => {
          if let Err(error) = bootrom.save_to_data_dir() {
            error!("Failed to save boot rom: {}", error);
          }
          *self = FrontendState::from_roms(Some(bootrom), cartridge.clone());
        }
        Err(e) => screen.set_error(format!("{}", e)),
      },
      FrontendState::InGame(state) => match Cartridge::from_path(path) {
        Ok(cartridge) => {
          *self = FrontendState::InGame(InGameState::from_config(HardwareConfig {
            cartridge,
            bootrom: state.config.bootrom.clone(),
            ..state.config
          }));
        }
        Err(e) => state.screen.set_error(format!("{}", e)),
      },
    }
  }
}

struct InGameState {
  config: HardwareConfig,
  machine: Machine,
  screen: gui::InGameScreen,
  fps_counter: FpsCounter,
  perf_counter: PerfCounter,
  delta: Duration,
  emu_time: EmuTime,
}

impl InGameState {
  pub fn from_config(config: HardwareConfig) -> InGameState {
    let machine = Machine::new(config.clone());
    let screen = gui::InGameScreen::new(&config);
    let fps_counter = FpsCounter::new();
    let perf_counter = PerfCounter::new();
    InGameState {
      config,
      emu_time: machine.emu_time(),
      machine,
      screen,
      fps_counter,
      perf_counter,
      delta: Duration::default(),
    }
  }
  pub fn update_delta_time(&mut self, delta: Duration) {
    self.delta = delta;
    let delta_s = delta.as_secs() as f64 + f64::from(delta.subsec_nanos()) / 1_000_000_000.0;
    self.fps_counter.update(delta_s);
    self.screen.fps = self.fps_counter.get_fps();
    self.screen.perf =
      100.0 * self.perf_counter.get_machine_cycles_per_s() * 4.0 / CPU_SPEED_HZ as f64;
  }
  pub fn tick(&mut self, renderer: &mut Renderer, ui: &imgui::Ui) {
    let delta_s =
      self.delta.as_secs() as f64 + f64::from(self.delta.subsec_nanos()) / 1_000_000_000.0;
    let machine_cycles =
      EmuTime::from_machine_cycles(((self.delta * CPU_SPEED_HZ as u32).as_secs() as u64) / 4);

    let target_time = self.emu_time + machine_cycles;
    loop {
      let (events, end_time) = self.machine.emulate(target_time);

      if events.contains(EmuEvents::VSYNC) {
        renderer.update_pixels(self.machine.screen_buffer());
      }

      if end_time >= target_time {
        self.perf_counter.update(end_time - self.emu_time, delta_s);
        self.emu_time = end_time;
        break;
      }
    }
    self.screen.render(ui);
  }
}

impl FrontendState {
  pub fn from_roms(bootrom: Option<Bootrom>, cartridge: Option<Cartridge>) -> FrontendState {
    use self::FrontendState::*;
    match (bootrom, cartridge) {
      (Some(bootrom), Some(cartridge)) => InGame(InGameState::from_config(HardwareConfig {
        model: bootrom.model,
        bootrom: Some(bootrom.data),
        cartridge,
      })),
      (None, Some(cartridge)) => WaitBootrom(Some(cartridge), gui::WaitBootromScreen::default()),
      (Some(bootrom), None) => InGame(InGameState::from_config(HardwareConfig {
        model: bootrom.model,
        bootrom: Some(bootrom.data),
        cartridge: Cartridge::no_cartridge(),
      })),
      _ => WaitBootrom(None, gui::WaitBootromScreen::default()),
    }
  }
}

pub fn run(bootrom: Option<Bootrom>, cartridge: Option<Cartridge>) -> Result<(), Error> {
  let mut state = FrontendState::from_roms(bootrom, cartridge);

  let mut gilrs = Gilrs::new().map_err(|_| anyhow!("Failed to initialize gamepad support"))?;

  let event_loop = EventLoop::new();

  let window = glutin::window::WindowBuilder::new()
    .with_min_inner_size(LogicalSize::new(160., 144.))
    .with_inner_size(LogicalSize::new(640., 576.))
    .with_title("Mooneye GB");

  let context = glutin::ContextBuilder::new()
    .with_hardware_acceleration(Some(true))
    .with_vsync(true)
    .with_srgb(true)
    .with_double_buffer(Some(true));

  let display = Display::new(window, context, &event_loop)?;

  let mut renderer = Renderer::new(&display)?;
  info!(
    "Initialized renderer with {}",
    match *display.get_opengl_version() {
      Version(Api::Gl, major, minor) => format!("OpenGL {}.{}", major, minor),
      Version(Api::GlEs, major, minor) => format!("OpenGL ES {}.{}", major, minor),
    }
  );

  let mut imgui = imgui::Context::create();
  imgui.set_ini_filename(None);
  imgui.set_log_filename(None);

  let mut user_interface = UserInterface::new(&mut imgui, &display)?;
  let mut frame_times = FrameTimes::new(Duration::from_secs(1) / 60);

  event_loop.run(move |event, _, control_flow| {
    *control_flow = ControlFlow::Poll;

    user_interface.handle_event(&mut imgui, &display, &event);
    match event {
      Event::NewEvents(_) => {
        let delta = frame_times.update();
        imgui.io_mut().update_delta_time(delta);
        state.update_delta_time(delta);
      }
      Event::MainEventsCleared => {
        while let Some(gilrs::Event { event, .. }) = gilrs.next_event() {
          state.handle_gilrs(event);
        }

        if let Err(e) = user_interface.prepare_frame(&mut imgui, &display) {
          error!("Failed to prepare frame: {}", e);
          *control_flow = ControlFlow::Exit;
          return;
        }
        display.gl_window().window().request_redraw();
      }
      Event::RedrawRequested(_) => {
        let ui = imgui.frame();

        let mut target = display.draw();
        target.clear_color_srgb(1.0, 1.0, 1.0, 1.0);

        state.tick(&mut renderer, &ui);
        renderer.draw(&mut target).expect("Failed to render");

        user_interface.prepare_render(&display, &ui);
        if let Err(e) = user_interface.render(&mut target, ui) {
          error!("Failed to render user interface: {}", e);
          *control_flow = ControlFlow::Exit;
        }
        if let Err(e) = target.finish() {
          error!("Failed to swap buffers: {}", e);
          *control_flow = ControlFlow::Exit;
        }
      }
      Event::RedrawEventsCleared => frame_times.limit(),
      Event::WindowEvent { event, .. } => match event {
        WindowEvent::Resized(..) => renderer.update_dimensions(&display),
        WindowEvent::DroppedFile(path) => state.drop_file(&path),
        WindowEvent::CloseRequested | WindowEvent::Destroyed => *control_flow = ControlFlow::Exit,
        WindowEvent::KeyboardInput { input, .. } => state.handle_keyboard(input),
        _ => (),
      },
      _ => (),
    }
  })
}

struct UserInterface {
  platform: imgui_winit_support::WinitPlatform,
  renderer: imgui_glium_renderer::Renderer,
}

impl UserInterface {
  pub fn new(imgui: &mut imgui::Context, display: &Display) -> Result<UserInterface, Error> {
    let mut platform = imgui_winit_support::WinitPlatform::init(imgui);
    let gl_window = display.gl_window();
    platform.attach_window(imgui.io_mut(), gl_window.window(), HiDpiMode::Default);

    let renderer = imgui_glium_renderer::Renderer::init(imgui, display)?;
    Ok(UserInterface { platform, renderer })
  }
  pub fn handle_event(&mut self, imgui: &mut imgui::Context, display: &Display, event: &Event<()>) {
    let gl_window = display.gl_window();
    self
      .platform
      .handle_event(imgui.io_mut(), gl_window.window(), &event);
  }
  pub fn prepare_frame(
    &mut self,
    imgui: &mut imgui::Context,
    display: &Display,
  ) -> Result<(), Error> {
    let gl_window = display.gl_window();
    gl_window.window().request_redraw();
    self
      .platform
      .prepare_frame(imgui.io_mut(), gl_window.window())?;
    Ok(())
  }
  pub fn prepare_render(&mut self, display: &Display, ui: &imgui::Ui) {
    self
      .platform
      .prepare_render(&ui, display.gl_window().window());
  }
  pub fn render<T: Surface>(&mut self, target: &mut T, ui: imgui::Ui) -> Result<(), Error> {
    let draw_data = ui.render();
    self.renderer.render(target, draw_data)?;
    Ok(())
  }
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

fn map_button(button: Button) -> Option<GbKey> {
  match button {
    Button::DPadRight => Some(GbKey::Right),
    Button::DPadLeft => Some(GbKey::Left),
    Button::DPadUp => Some(GbKey::Up),
    Button::DPadDown => Some(GbKey::Down),
    Button::South => Some(GbKey::B),
    Button::East => Some(GbKey::A),
    Button::Start => Some(GbKey::Start),
    Button::Select => Some(GbKey::Select),
    _ => None,
  }
}

fn map_axis(axis: Axis, value: f32) -> Option<(GbKey, bool)> {
  match axis {
    Axis::LeftStickX => {
      if value < -0.5 {
        Some((GbKey::Left, true))
      } else if value < 0.0 {
        Some((GbKey::Left, false))
      } else if value < 0.5 {
        Some((GbKey::Right, false))
      } else {
        Some((GbKey::Right, true))
      }
    }
    Axis::LeftStickY => {
      if value < -0.5 {
        Some((GbKey::Up, true))
      } else if value < 0.0 {
        Some((GbKey::Up, false))
      } else if value < 0.5 {
        Some((GbKey::Down, false))
      } else {
        Some((GbKey::Down, true))
      }
    }
    _ => None,
  }
}
