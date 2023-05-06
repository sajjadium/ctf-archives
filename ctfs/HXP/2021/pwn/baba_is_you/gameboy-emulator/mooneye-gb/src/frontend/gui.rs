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
use imgui::{im_str, Condition, ImString, StyleColor, StyleVar, Ui, Window};
use std::time::Instant;

use mooneye_gb::config::HardwareConfig;

pub trait Screen {
  fn render(&mut self, ui: &Ui<'_>);
}

#[derive(Default)]
pub struct WaitBootromScreen {
  error: Option<ImString>,
}

impl WaitBootromScreen {
  pub fn set_error(&mut self, text: String) {
    self.error = Some(ImString::new(text));
  }
}

impl Screen for WaitBootromScreen {
  fn render(&mut self, ui: &Ui<'_>) {
    Window::new(im_str!("Help overlay"))
      .title_bar(false)
      .resizable(false)
      .movable(false)
      .always_auto_resize(true)
      .position([0.0, 0.0], Condition::Always)
      .build(ui, || {
        ui.text("Mooneye GB requires a boot ROM to run");
        ui.text("Drag and drop here a boot rom of one of these types:");
        ui.bullet_text(im_str!("Game Boy (usually called dmg_boot.bin)"));
        ui.bullet_text(im_str!("Game Boy Pocket (usually called mgb_boot.bin)"));

        if let Some(ref error) = self.error {
          ui.separator();
          ui.text_colored([1.0, 0.0, 0.0, 1.0], &error);
        }
      });
  }
}

pub struct ErrorOverlay {
  error: ImString,
  appear_timestamp: Instant,
}

impl ErrorOverlay {
  fn from_error(error: String) -> ErrorOverlay {
    ErrorOverlay {
      error: ImString::new(error),
      appear_timestamp: Instant::now(),
    }
  }
  fn render(&self, ui: &Ui<'_>) -> bool {
    let elapsed = self.appear_timestamp.elapsed();
    let bg = ui.push_style_color(StyleColor::WindowBg, [1.0, 1.0, 1.0, 0.4]);
    let border = ui.push_style_var(StyleVar::WindowBorderSize(1.0));
    Window::new(im_str!("Error overlay"))
      .title_bar(false)
      .resizable(false)
      .movable(false)
      .always_auto_resize(true)
      .position([0.0, 0.0], Condition::Always)
      .build(ui, || {
        ui.text_colored([1.0, 0.0, 0.0, 1.0], &self.error);
      });
    border.pop(ui);
    bg.pop(ui);
    elapsed.as_secs() < 5
  }
}

pub struct InGameScreen {
  pub fps: f64,
  pub perf: f64,
  model: ImString,
  cartridge_title: ImString,
  show_info_overlay: bool,
  error_overlay: Option<ErrorOverlay>,
}

impl InGameScreen {
  pub fn new(config: &HardwareConfig) -> InGameScreen {
    InGameScreen {
      fps: 0.0,
      perf: 0.0,
      model: ImString::new(format!("{}", config.model)),
      cartridge_title: ImString::new(config.cartridge.title.clone()),
      show_info_overlay: false,
      error_overlay: None,
    }
  }
  pub fn toggle_info_overlay(&mut self) {
    self.show_info_overlay = !self.show_info_overlay;
  }
  pub fn set_error(&mut self, err: String) {
    self.error_overlay = Some(ErrorOverlay::from_error(err));
  }
}

impl Screen for InGameScreen {
  fn render(&mut self, ui: &Ui<'_>) {
    if self.show_info_overlay {
      let bg = ui.push_style_color(StyleColor::WindowBg, [0.0, 0.0, 0.0, 0.4]);
      Window::new(im_str!("Info overlay"))
        .title_bar(false)
        .resizable(false)
        .movable(false)
        .always_auto_resize(true)
        .position([0.0, 0.0], Condition::Always)
        .build(ui, || {
          ui.text(&self.model);
          ui.text(&self.cartridge_title);
          ui.text(format!("FPS: {:.0}, speed: {:.0} %", self.fps, self.perf));
        });
      bg.pop(ui);
    }
    if let Some(overlay) = self.error_overlay.take() {
      if overlay.render(ui) {
        self.error_overlay = Some(overlay);
      }
    }
  }
}
