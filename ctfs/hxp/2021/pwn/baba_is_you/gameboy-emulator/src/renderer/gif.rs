use std::{borrow::Cow, fs::File};

use gif::{Encoder, Frame, Repeat};
use mooneye_gb::{ScreenBuffer, SCREEN_HEIGHT, SCREEN_WIDTH};

use super::Renderer;

pub struct GifRenderer {
    encoder: Encoder<File>,
    buffer: [u8; SCREEN_WIDTH * SCREEN_HEIGHT],
    frame_skip: usize,
    frame_i: usize,
}

impl GifRenderer {
    pub fn new(frame_skip: usize) -> GifRenderer {
        let color_map = &[255, 247, 123, 181, 174, 74, 107, 105, 49, 32, 32, 16];
        let image = File::create("playback.gif").unwrap();
        let mut encoder =
            Encoder::new(image, SCREEN_WIDTH as u16, SCREEN_HEIGHT as u16, color_map).unwrap();
        encoder.set_repeat(Repeat::Infinite).unwrap();
        GifRenderer {
            encoder,
            buffer: [0; SCREEN_WIDTH * SCREEN_HEIGHT],
            frame_skip,
            frame_i: 0,
        }
    }
}

impl Renderer for GifRenderer {
    fn update_pixels(&mut self, pixels: &ScreenBuffer) {
        self.buffer.iter_mut().for_each(|x| *x = 0);
        for (y, line) in pixels.chunks(SCREEN_WIDTH).enumerate() {
            for (x, pixel) in line.iter().enumerate() {
                self.buffer[y * SCREEN_WIDTH + x] = *pixel as u8;
            }
        }
        if self.frame_i == 0 {
            self.force_draw();
        }

        self.frame_i = (self.frame_i + 1) % (self.frame_skip + 1);
    }

    /// Force a print to stdout. Used to print the very last frame so it isn't skipped.
    fn force_draw(&mut self) {
        let mut frame = Frame {
            // Set to something > 1: https://superuser.com/a/569967
            delay: 4, // => 25 fps
            width: SCREEN_WIDTH as u16,
            height: SCREEN_HEIGHT as u16,
            ..Default::default()
        };
        frame.buffer = Cow::Borrowed(&self.buffer);
        self.encoder.write_frame(&frame).unwrap();
        // println!("{}", self.canvas.frame());
    }
}
