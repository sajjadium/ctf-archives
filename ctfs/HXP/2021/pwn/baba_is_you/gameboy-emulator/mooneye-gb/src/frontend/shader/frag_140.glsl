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
#version 140

uniform sampler2D tex_front;
uniform sampler2D tex_back;
uniform mat4 palette;

in vec2 v_tex_coords;
out vec4 f_color;

void main() {
  float color_front = texture(tex_front, v_tex_coords).x;
  float color_back = texture(tex_back, v_tex_coords).x;
  float color = mix(color_front, color_back, 0.5);
  f_color = palette[uint(color * 255.0 + 0.5)];
}
