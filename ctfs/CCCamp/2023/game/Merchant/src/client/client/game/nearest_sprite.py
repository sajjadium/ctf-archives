from typing import Tuple, TypedDict

import pyglet
from pyglet import graphics
from pyglet.gl import (
    GL_CLAMP_TO_EDGE,
    GL_NEAREST,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_SRC_ALPHA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_TRIANGLES,
    glTexParameteri,
)
from pyglet.graphics import Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.image import Animation, Texture
from pyglet.sprite import AdvancedSprite

vertex_source = """#version 150 core
    in vec3 translate;
    in vec4 colors;
    in vec3 tex_coords;
    in vec2 scale;
    in vec3 position;
    in float rotation;

    out vec4 vertex_colors;
    out vec3 texture_coords;

    uniform vec2 origin_scale;
    uniform vec2 origin_rotation;

    uniform WindowBlock
    {
        mat4 projection;
        mat4 view;
    } window;

    mat4 m_scale = mat4(1.0);
    mat4 m_rotation = mat4(1.0);
    mat4 m_translate = mat4(1.0);
    mat4 m_origin_scale = mat4(1.0);
    mat4 m_neg_origin_scale = mat4(1.0);
    mat4 m_origin_rotation = mat4(1.0);
    mat4 m_neg_origin_rotation = mat4(1.0);

    void main()
    {
        m_scale[0][0] = scale.x;
        m_scale[1][1] = scale.y;
        m_translate[3][0] = translate.x;
        m_translate[3][1] = translate.y;
        m_translate[3][2] = translate.z;
        
        m_origin_scale[3][0] = origin_scale.x;
        m_origin_scale[3][1] = origin_scale.y;

        m_neg_origin_scale[3][0] = -origin_scale.x;
        m_neg_origin_scale[3][1] = -origin_scale.y;
        
        m_origin_rotation[3][0] = origin_rotation.x;
        m_origin_rotation[3][1] = origin_rotation.y;

        m_neg_origin_rotation[3][0] = -origin_rotation.x;
        m_neg_origin_rotation[3][1] = -origin_rotation.y;
        
        m_rotation[0][0] =  cos(-radians(rotation)); 
        m_rotation[0][1] =  sin(-radians(rotation));
        m_rotation[1][0] = -sin(-radians(rotation));
        m_rotation[1][1] =  cos(-radians(rotation));

        gl_Position = window.projection * window.view * m_translate * m_origin_rotation * m_rotation * m_neg_origin_rotation * m_origin_scale * m_scale * m_neg_origin_scale * vec4(position, 1.0);

        vertex_colors = colors;
        texture_coords = tex_coords;
    }
"""

fragment_source = """#version 150 core
    in vec4 vertex_colors;
    in vec3 texture_coords;
    out vec4 final_colors;

    uniform sampler2D sprite_texture;

    void main()
    {
        final_colors = texture(sprite_texture, texture_coords.xy) * vertex_colors;
    }
"""


def get_default_shader() -> ShaderProgram:
    try:
        return pyglet.gl.current_context._game_sprite_default_shader  # type: ignore
    except AttributeError:
        _default_vert_shader = graphics.shader.Shader(vertex_source, "vertex")
        _default_frag_shader = graphics.shader.Shader(fragment_source, "fragment")
        default_shader_program = graphics.shader.ShaderProgram(
            _default_vert_shader, _default_frag_shader
        )
        pyglet.gl.current_context.game_sprite_default_shader = (  # type: ignore
            default_shader_program
        )
        return pyglet.gl.current_context.game_sprite_default_shader  # type: ignore


class RequestParams(TypedDict, total=False):
    pass


class NearestSprite(AdvancedSprite):
    origin: Tuple[float, float]

    def __init__(
        self,
        img: Texture | Animation,
        x: int = 0,
        y: int = 0,
        z: int = 0,
        origin: Tuple[float, float] = (0, 0),
        origin_scale: Tuple[float, float] = (0, 0),
        origin_rotation: Tuple[float, float] = (0, 0),
        blend_src: int = GL_SRC_ALPHA,
        blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
        # never ever give this a batch, this would use the default shader and break things! you have to call .draw yourself
        group: Group | None = None,
        subpixel: bool = False,
    ):
        if origin != (0, 0):
            self.origin_scale = origin
            self.origin_rotation = origin

            assert origin_scale == (0, 0)
            assert origin_rotation == (0, 0)
        else:
            self.origin_scale = origin_scale
            self.origin_rotation = origin_rotation

        super().__init__(
            img,
            x,
            y,
            z,
            blend_src,
            blend_dest,
            None,
            group,
            subpixel,
            get_default_shader(),
        )

    def draw(self):
        """Draw the sprite at its current position.

        See the module documentation for hints on drawing multiple sprites
        efficiently.
        """
        if not self._group:
            return

        self._group.set_state_recursive()
        if self.program:
            self.program["origin_scale"] = (self.origin_scale[0], self.origin_scale[1])
            self.program["origin_rotation"] = (
                self.origin_rotation[0],
                self.origin_rotation[1],
            )

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        if self._vertex_list:
            self._vertex_list.draw(GL_TRIANGLES)

        self._group.unset_state_recursive()
