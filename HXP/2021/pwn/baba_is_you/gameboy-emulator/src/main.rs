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

mod frame_times;
mod renderer;
mod replay;
mod state;

use std::{
    path::{Path, PathBuf},
    str::FromStr,
    sync::Arc,
    time::{Duration, Instant},
};

use anyhow::{anyhow, Context, Error, Result};
use clap::Parser;
use glium::{
    glutin,
    glutin::{
        event::{Event, WindowEvent},
        event_loop::{ControlFlow, EventLoop},
    },
    Display, Surface,
};
use mooneye_gb::config::{Bootrom, Cartridge, HardwareConfig};
// NOTE: Using this since std's Mutex isn't fair and may not let our ctrl+c handler get the lock
use parking_lot::Mutex;

use frame_times::FrameTimes;
use renderer::{GifRenderer, OpenGlRenderer, Renderer as RendererTrait, TerminalRenderer};
use replay::{KeysLog, ReplayMode};
use state::State;

const GB_KEYS: usize = 8;

#[derive(Parser)]
struct Cli {
    #[clap(short = 's', long, default_value = "1.0")]
    emulation_speed: f64,
    #[clap(short = 'c', long, default_value = "main.gb")]
    cartridge: PathBuf,
    #[clap(subcommand)]
    sub_cmd: SubCommand,
}

#[derive(Parser)]
enum SubCommand {
    /// Record a replay
    Record {
        /// Path for replay file to be written to
        path: PathBuf,
    },
    /// Playback a replay
    Playback {
        /// Path for replay file to be read from; Set to 'STDIN' to read base64 encoded replay from
        /// stdin
        path: PathBuf,
        /// Choose renderer. Possible values: 'opengl', 'terminal' or 'gif'.
        /// Use something like 'terminal:10' or 'gif:6' to enable frame skipping.
        #[clap(short = 'r', long, default_value = "opengl")]
        renderer: Renderer,
    },
}

#[derive(Parser, Clone, Copy)]
enum Renderer {
    OpenGl,
    Terminal { frame_skip: usize },
    Gif { frame_skip: usize },
}

impl FromStr for Renderer {
    type Err = Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s.split(':');
        match parts.next().unwrap() {
            "opengl" => Ok(Renderer::OpenGl),
            "terminal" => Ok(Renderer::Terminal {
                frame_skip: parts.next().unwrap_or("0").parse()?,
            }),
            "gif" => Ok(Renderer::Gif {
                frame_skip: parts.next().unwrap_or("0").parse()?,
            }),
            _ => Err(anyhow!("invalid renderer value")),
        }
    }
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    let (replay, renderer) = match &cli.sub_cmd {
        SubCommand::Record { path } => (
            ReplayMode::Record {
                keys_log: KeysLog::new(),
                path: path.to_owned(),
            },
            Renderer::OpenGl,
        ),
        SubCommand::Playback { path, renderer } => {
            let keys_log = if path == Path::new("STDIN") {
                KeysLog::read_from_stdin()?
            } else {
                KeysLog::read_from_file(path)?
            };
            (
                ReplayMode::Playback {
                    keys_log,
                    current: 0,
                },
                *renderer,
            )
        }
    };

    let bootrom = Bootrom::from_path(Path::new("dmg_boot.bin")).context("Missing dmg_boot.bin")?;
    let cartridge = Cartridge::from_path(&cli.cartridge).context("Failed to load cartridge")?;

    let hardware_config = HardwareConfig {
        model: bootrom.model,
        bootrom: Some(bootrom.data),
        cartridge,
    };
    let state = Arc::new(Mutex::new(State::from_config(hardware_config, replay)));

    let state_clone = Arc::clone(&state);
    ctrlc::set_handler(move || {
        do_exit(&state_clone.lock());
    })?;

    let frame_times = FrameTimes::new(Duration::from_secs(1) / 60);
    let emulation_speed = cli.emulation_speed;
    match renderer {
        Renderer::OpenGl => run_opengl(emulation_speed, frame_times, state),
        Renderer::Terminal { frame_skip } => run_terminal(
            TerminalRenderer::new(frame_skip),
            emulation_speed,
            frame_times,
            state,
        ),
        Renderer::Gif { frame_skip } => run_terminal(
            GifRenderer::new(frame_skip),
            emulation_speed,
            frame_times,
            state,
        ),
    }
}

// Returns false if replay playback ended
#[must_use]
fn advance_state<R: renderer::Renderer>(
    emu_speed: f64,
    renderer: &mut R,
    state: &mut State,
    frame_times: &mut FrameTimes,
) -> bool {
    // Limit iterations so we don't get stuck here indefinitely even if we're emulating too slowly
    let mut iterations = 0;
    while frame_times.target_render_time() <= Instant::now() && iterations < 6 {
        state.delta = frame_times.update(emu_speed);
        if !state.tick(renderer) {
            // Force redraw in case the renderer is skipping frames
            renderer.force_draw();

            println!("Replay ended!");
            match state.ticks_until_flag {
                None => println!("No flag :("),
                Some(n) => println!("{} steps until flag!", n),
            }
            return false;
        }
        iterations += 1
    }
    true
}

fn run_terminal<R: RendererTrait>(
    mut renderer: R,
    emu_speed: f64,
    mut frame_times: FrameTimes,
    state: Arc<Mutex<State>>,
) -> Result<()> {
    loop {
        {
            let mut state = state.lock();
            if !advance_state(emu_speed, &mut renderer, &mut state, &mut frame_times) {
                do_exit(&state);
            }
        }
        // Sleep so we don't busy wait until we're ready to advance the state
        let now = Instant::now();
        if frame_times.target_render_time() > now {
            std::thread::sleep(frame_times.target_render_time() - now);
        }
    }
}

fn run_opengl(emu_speed: f64, mut frame_times: FrameTimes, state: Arc<Mutex<State>>) -> Result<()> {
    let event_loop = EventLoop::new();

    let window = glutin::window::WindowBuilder::new()
        .with_title("hxp Gameboy Emulator - powered by Mooneye GB");
    let context = glutin::ContextBuilder::new();
    let display = Display::new(window, context, &event_loop)?;

    let mut renderer = OpenGlRenderer::new(&display)?;

    event_loop.run(move |event, _, control_flow| {
        *control_flow = ControlFlow::Poll;
        match event {
            Event::MainEventsCleared => {
                display.gl_window().window().request_redraw();
            }
            Event::RedrawRequested(_) => {
                let mut target = display.draw();
                target.clear_color_srgb(1.0, 1.0, 1.0, 1.0);

                let mut state = state.lock();
                if !advance_state(emu_speed, &mut renderer, &mut state, &mut frame_times) {
                    *control_flow = ControlFlow::Exit;
                }

                renderer.draw(&mut target).expect("Failed to render");
                if let Err(e) = target.finish() {
                    println!("Failed to swap buffers: {}", e);
                    *control_flow = ControlFlow::Exit;
                }
            }
            Event::RedrawEventsCleared => {
                *control_flow = ControlFlow::WaitUntil(frame_times.target_render_time())
            }
            Event::WindowEvent { event, .. } => match event {
                WindowEvent::Resized(..) => renderer.update_dimensions(&display),
                WindowEvent::CloseRequested | WindowEvent::Destroyed => {
                    *control_flow = ControlFlow::Exit;
                }
                WindowEvent::KeyboardInput { input, .. } => state.lock().handle_keyboard(input),
                _ => (),
            },
            Event::LoopDestroyed => {
                do_exit(&state.lock());
            }
            _ => (),
        }
    });
}

fn do_exit(state: &State) -> ! {
    if let ReplayMode::Record { keys_log, path } = &state.replay_mode {
        println!("Saving replay to {}", path.display());
        keys_log.save_to_file(path).expect("failed to save replay");
    }
    std::process::exit(0);
}
