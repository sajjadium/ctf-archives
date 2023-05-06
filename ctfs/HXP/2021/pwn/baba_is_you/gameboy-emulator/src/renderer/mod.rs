mod gif;
mod opengl;
mod terminal;

pub use self::gif::GifRenderer;
pub use opengl::OpenGlRenderer;
pub use terminal::TerminalRenderer;

use mooneye_gb::ScreenBuffer;

pub trait Renderer {
    fn update_pixels(&mut self, pixels: &ScreenBuffer);

    fn force_draw(&mut self) {}
}
