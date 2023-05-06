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
use anyhow::Error;
use glium::backend::Facade;
use glium::index::PrimitiveType;
use glium::texture::pixel_buffer::PixelBuffer;
use glium::texture::texture2d::Texture2d;
use glium::texture::{MipmapsOption, UncompressedFloatFormat};
use glium::uniforms::{MagnifySamplerFilter, MinifySamplerFilter};
use glium::{implement_vertex, program, uniform};
use glium::{DrawParameters, IndexBuffer, Program, Surface, VertexBuffer};
use mooneye_gb;
use nalgebra::{Matrix4, Vector4};

type Texture = Texture2d;

#[derive(Copy, Clone)]
pub struct Vertex {
  position: [f32; 2],
  tex_coords: [f32; 2],
}

implement_vertex!(Vertex, position, tex_coords);

pub struct Renderer {
  vertex_buffer: VertexBuffer<Vertex>,
  index_buffer: IndexBuffer<u16>,
  pixel_buffer: PixelBuffer<u8>,
  program: Program,
  texture_even: Texture,
  texture_odd: Texture,
  matrix: Matrix4<f32>,
  palette: Matrix4<f32>,
  frame_state: FrameState,
}

#[derive(Copy, Clone, Debug, Eq, PartialEq)]
enum FrameState {
  Even,
  Odd,
}

impl FrameState {
  fn flip(&mut self) {
    *self = match self {
      FrameState::Even => FrameState::Odd,
      FrameState::Odd => FrameState::Even,
    }
  }
}

const TEXTURE_WIDTH: u32 = 256;
const TEXTURE_HEIGHT: u32 = 256;
const TEX_OFFSET_X: f32 = mooneye_gb::SCREEN_WIDTH as f32 / TEXTURE_WIDTH as f32;
const TEX_OFFSET_Y: f32 = mooneye_gb::SCREEN_HEIGHT as f32 / TEXTURE_HEIGHT as f32;

fn upload_pixels(texture: &mut Texture, pixel_buffer: &PixelBuffer<u8>) {
  texture.main_level().raw_upload_from_pixel_buffer(
    pixel_buffer.as_slice(),
    0..mooneye_gb::SCREEN_WIDTH as u32,
    0..mooneye_gb::SCREEN_HEIGHT as u32,
    0..1,
  );
}

const ASPECT_RATIO: f32 = mooneye_gb::SCREEN_WIDTH as f32 / mooneye_gb::SCREEN_HEIGHT as f32;

fn aspect_ratio_correction(width: u32, height: u32) -> (f32, f32) {
  let fb_aspect_ratio = width as f32 / height as f32;
  let scale = ASPECT_RATIO / fb_aspect_ratio;
  if fb_aspect_ratio >= ASPECT_RATIO {
    (scale, 1.0)
  } else {
    (1.0, 1.0 / scale)
  }
}

impl Renderer {
  pub fn new<F: Facade>(display: &F) -> Result<Renderer, Error> {
    let vertexes = [
      Vertex {
        position: [-1.0, -1.0],
        tex_coords: [0.0, TEX_OFFSET_Y],
      },
      Vertex {
        position: [-1.0, 1.0],
        tex_coords: [0.0, 0.0],
      },
      Vertex {
        position: [1.0, 1.0],
        tex_coords: [TEX_OFFSET_X, 0.0],
      },
      Vertex {
        position: [1.0, -1.0],
        tex_coords: [TEX_OFFSET_X, TEX_OFFSET_Y],
      },
    ];

    let vertex_buffer = VertexBuffer::immutable(display, &vertexes)?;

    let index_buffer =
      IndexBuffer::immutable(display, PrimitiveType::TriangleStrip, &[1u16, 2, 0, 3])?;

    let program = program!(
      display,
      140 => {
        vertex: include_str!("shader/vert_140.glsl"),
        fragment: include_str!("shader/frag_140.glsl"),
        outputs_srgb: true
      },
      110 => {
        vertex: include_str!("shader/vert_110.glsl"),
        fragment: include_str!("shader/frag_110.glsl"),
        outputs_srgb: true
      }
    )?;

    let pixel_buffer = PixelBuffer::new_empty(
      display,
      mooneye_gb::SCREEN_WIDTH * mooneye_gb::SCREEN_HEIGHT,
    );
    pixel_buffer.write(&[0; mooneye_gb::SCREEN_PIXELS]);

    let mut texture_even = Texture::empty_with_format(
      display,
      UncompressedFloatFormat::U8,
      MipmapsOption::NoMipmap,
      TEXTURE_WIDTH,
      TEXTURE_HEIGHT,
    )?;
    let mut texture_odd = Texture::empty_with_format(
      display,
      UncompressedFloatFormat::U8,
      MipmapsOption::NoMipmap,
      TEXTURE_WIDTH,
      TEXTURE_HEIGHT,
    )?;
    upload_pixels(&mut texture_even, &pixel_buffer);
    upload_pixels(&mut texture_odd, &pixel_buffer);

    let (width, height) = display.get_context().get_framebuffer_dimensions();
    let (x_scale, y_scale) = aspect_ratio_correction(width, height);
    let matrix = Matrix4::from_diagonal(&Vector4::new(x_scale, y_scale, 1.0, 1.0));

    let palette = Matrix4::new(
      255.0, 181.0, 107.0, 33.0, 247.0, 174.0, 105.0, 32.0, 123.0, 74.0, 49.0, 16.0, 1.0, 1.0, 1.0,
      1.0,
    ) / 255.0;

    Ok(Renderer {
      vertex_buffer,
      index_buffer,
      pixel_buffer,
      program,
      texture_even,
      texture_odd,
      matrix,
      palette,
      frame_state: FrameState::Even,
    })
  }

  pub fn draw<S: Surface>(&self, frame: &mut S) -> Result<(), Error> {
    let matrix: &[[f32; 4]; 4] = self.matrix.as_ref();
    let palette: &[[f32; 4]; 4] = self.palette.as_ref();

    let (tex_front, tex_back) = match self.frame_state {
      FrameState::Even => (&self.texture_even, &self.texture_odd),
      FrameState::Odd => (&self.texture_odd, &self.texture_even),
    };

    let uniforms = uniform! {
      matrix: *matrix,
      palette: *palette,
      tex_front: tex_front.sampled()
        .minify_filter(MinifySamplerFilter::Nearest)
        .magnify_filter(MagnifySamplerFilter::Nearest),
      tex_back: tex_back.sampled()
        .minify_filter(MinifySamplerFilter::Nearest)
        .magnify_filter(MagnifySamplerFilter::Nearest),
    };

    let params = DrawParameters {
      ..Default::default()
    };
    frame.draw(
      &self.vertex_buffer,
      &self.index_buffer,
      &self.program,
      &uniforms,
      &params,
    )?;
    Ok(())
  }
  pub fn update_dimensions<F: Facade>(&mut self, display: &F) {
    let (width, height) = display.get_context().get_framebuffer_dimensions();
    let (x_scale, y_scale) = aspect_ratio_correction(width, height);
    self.matrix.m11 = x_scale;
    self.matrix.m22 = y_scale;
  }
  pub fn update_pixels(&mut self, pixels: &mooneye_gb::ScreenBuffer) {
    let mut buffer = [0u8; mooneye_gb::SCREEN_PIXELS];
    for idx in 0..mooneye_gb::SCREEN_PIXELS {
      buffer[idx] = pixels[idx] as u8;
    }
    self.pixel_buffer.write(&buffer);
    self.frame_state.flip();
    let texture = match self.frame_state {
      FrameState::Odd => &mut self.texture_odd,
      FrameState::Even => &mut self.texture_even,
    };
    upload_pixels(texture, &self.pixel_buffer);
  }
}
