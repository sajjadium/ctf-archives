use drawille::Canvas;
use mooneye_gb::{Color, ScreenBuffer, SCREEN_HEIGHT, SCREEN_WIDTH};

use super::Renderer;

pub struct TerminalRenderer {
    canvas: Canvas,
    frame_skip: usize,
    frame_i: usize,
}

impl TerminalRenderer {
    pub fn new(frame_skip: usize) -> TerminalRenderer {
        TerminalRenderer {
            canvas: Canvas::new(SCREEN_WIDTH as _, SCREEN_HEIGHT as _),
            frame_skip,
            frame_i: 0,
        }
    }
}

impl Renderer for TerminalRenderer {
    fn update_pixels(&mut self, pixels: &ScreenBuffer) {
        self.canvas.clear();
        for (y, line) in pixels.chunks(SCREEN_WIDTH).enumerate() {
            for (x, pixel) in line.iter().enumerate() {
                if *pixel != Color::Off {
                    self.canvas.set(x as _, y as _);
                }
            }
        }
        if self.frame_i == 0 {
            self.force_draw();
        }
        self.frame_i = (self.frame_i + 1) % (self.frame_skip + 1);
    }

    /// Force a print to stdout. Used to print the very last frame so it isn't skipped.
    fn force_draw(&mut self) {
        println!("{}", self.canvas.frame());
    }
}
