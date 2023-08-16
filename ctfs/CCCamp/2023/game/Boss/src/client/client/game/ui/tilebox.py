import logging
from functools import cache

from pyglet.gl import (
    GL_BLEND,
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
    glBlendFunc,
    glDisable,
    glEnable,
    glTexParameteri,
)
from pyglet.graphics import Group
from pyglet.graphics.shader import Shader, ShaderProgram

from client.game.ui import get_ui_image

TILE_SIZE_X = 16
TILE_SIZE_Y = 16

VERTEX_SOURCE = """#version 330 core
    in vec2 tex_coords;
    in vec2 position;
    out vec2 texture_pos;
    out vec3 vertex_colors;

    uniform vec2 translation;
    uniform vec2 scale;
    uniform vec3 color_add;
    uniform bool center;

    uniform WindowBlock 
    {                       // This UBO is defined on Window creation, and available
        mat4 projection;    // in all Shaders. You can modify these matrixes with the
        mat4 view;          // Window.view and Window.projection properties.
    } window;

    mat4 m_translate = mat4(1.0);
    mat4 m_scale = mat4(1.0);

    void main()
    {
        m_translate[3][0] = translation.x;
        m_translate[3][1] = translation.y;
        m_scale[0][0] = scale.x;
        m_scale[1][1] = scale.y;
        gl_Position = window.projection * window.view * m_translate * m_scale * vec4(position, 0, 1);
        texture_pos = tex_coords;
        vertex_colors = color_add;
    }
"""

FRAGMENT_SOURCE = """#version 330 core
    in vec2 texture_pos;
    in vec3 vertex_colors;
    out vec4 final_color;
    uniform sampler2D texture_atlas;

    void main()
    {
        vec4 tex_color = texture(texture_atlas, texture_pos);
        final_color = tex_color + vec4(vertex_colors, 0) *tex_color.w;
    }
"""


@cache
def get_tile_box_shader() -> ShaderProgram:
    logging.debug("Map Shader Recalc")
    vert_shader = Shader(VERTEX_SOURCE, "vertex")
    frag_shader = Shader(FRAGMENT_SOURCE, "fragment")
    return ShaderProgram(vert_shader, frag_shader)


def create_quad(
    x: float, y: float, ts: int
) -> tuple[float, float, float, float, float, float, float, float]:
    x = x * ts
    y = y * ts
    x2 = x + ts
    y2 = y + ts
    return (x, y, x2, y, x2, y2, x, y2)


def create_quad_tex(
    x: float, y: float, w: float, h: float
) -> tuple[float, float, float, float, float, float, float, float]:
    x = x * TILE_SIZE_X
    y = y * TILE_SIZE_Y
    x2 = x + TILE_SIZE_X
    y2 = y + TILE_SIZE_Y
    x /= w
    x2 /= w
    y /= h
    y2 /= h
    y = 1 - y
    y2 = 1 - y2

    return (x, y2, x2, y2, x2, y, x, y)


def gen_quad_indices(n: int) -> tuple[int, int, int, int, int, int]:
    offset = n * 4
    return (0 + offset, 1 + offset, 2 + offset, 0 + offset, 2 + offset, 3 + offset)


class TileStrip(Group):
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        tile_size: int = 32,
        tile_offset_x: int = 0,
        tile_offset_y: int = 0,
        scale_x: float = 1,
        scale_y: float = 1,
        group: Group | None = None,
        horizontal: bool = True,
    ):
        self.color_add: tuple[float, float, float] = (0, 0, 0)
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.tile_offset_x = tile_offset_x
        self.tile_offset_y = tile_offset_y
        self.tile_size = tile_size
        self.width = width - width % -tile_size
        self.width = max(tile_size * 3, self.width)
        self.height = height - height % -tile_size
        self.x = x
        self.y = y
        self.horizontal = horizontal
        self.vlist = None
        self.program = get_tile_box_shader()

        super().__init__(parent=group)

    def set_state(self):
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.program.use()
        self.texture.bind(0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        glDisable(GL_BLEND)
        self.program.stop()
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw(self):
        if self.vlist is None:
            image = get_ui_image()
            self.texture = image.get_texture()

            position: list[float] = []
            indices: list[int] = []
            tex_coords: list[float] = []

            match self.horizontal:
                case True:
                    for x in range(int(self.width // self.tile_size)):
                        position += create_quad(
                            x=x - (self.width // self.tile_size) / 2,
                            y=-0.5,
                            ts=self.tile_size,
                        )
                        indices += gen_quad_indices(x)

                        tile_offset_x = 0

                        if x > 0:
                            tile_offset_x += 1
                        if x == self.width // self.tile_size - 1:
                            tile_offset_x += 1

                        tex_coords += create_quad_tex(
                            self.tile_offset_x + tile_offset_x,
                            self.tile_offset_y,
                            image.width,
                            image.height,
                        )
                case False:
                    for y in range(int(self.height // self.tile_size)):
                        position += create_quad(
                            x=-0.5,
                            y=y - (self.height // self.tile_size) / 2,
                            ts=self.tile_size,
                        )
                        indices += gen_quad_indices(y)

                        tile_offset_y = 0

                        if y > 0:
                            tile_offset_y -= 1
                        if y == self.height // self.tile_size - 1:
                            tile_offset_y -= 1

                        tex_coords += create_quad_tex(
                            self.tile_offset_x,
                            self.tile_offset_y + tile_offset_y,
                            image.width,
                            image.height,
                        )

            self.vlist = self.program.vertex_list_indexed(
                4 * (self.width // self.tile_size) * (self.height // self.tile_size),
                GL_TRIANGLES,
                indices,
                position=("f", position),
                tex_coords=("f", tex_coords),
            )
        self.program["translation"] = (
            self.x + self.width / 2,
            self.y + self.height / 2,
        )
        self.program["scale"] = (self.scale_x, self.scale_y)
        self.program["color_add"] = self.color_add
        # self.program["center"] = center
        self.set_state_recursive()
        self.vlist.draw(GL_TRIANGLES)
        self.unset_state_recursive()


class TileBox(Group):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: tuple[int, int, int, int] = (80, 0, 80, 255),
        tile_size: int = 32,
        tile_offset_x: int = 0,
        tile_offset_y: int = 0,
        scale_x: float = 1,
        scale_y: float = 1,
        group: Group | None = None,
    ):
        self.scale_x = scale_y
        self.scale_y = scale_x
        self.tile_size = tile_size
        self.width = (width // tile_size) * tile_size
        self.height = (height // tile_size) * tile_size
        self.x = x
        self.y = y
        self.vlist = None
        self.tile_offset_x = tile_offset_x
        self.tile_offset_y = tile_offset_y
        self.program = get_tile_box_shader()

        super().__init__(parent=group)

    def set_state(self):
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.program.use()
        self.texture.bind(0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        glDisable(GL_BLEND)
        self.program.stop()
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw(self):
        if self.vlist is None:
            image = get_ui_image()
            self.texture = image.get_texture()

            position: list[float] = []
            indices: list[int] = []
            tex_coords: list[float] = []
            for x in range(int(self.width // self.tile_size)):
                for y in range(int(self.height // self.tile_size)):
                    position += create_quad(x, y, self.tile_size)
                    indices += gen_quad_indices(
                        int(self.width // self.tile_size) * y + x
                    )
                    tile_offset_x = 0
                    tile_offset_y = 2
                    if x > 0:
                        tile_offset_x += 1
                    if x == self.width // self.tile_size - 1:
                        tile_offset_x += 1
                    if y > 0:
                        tile_offset_y -= 1
                    if y == self.height // self.tile_size - 1:
                        tile_offset_y -= 1
                    tex_coords += create_quad_tex(
                        self.tile_offset_x + tile_offset_x,
                        self.tile_offset_y + tile_offset_y,
                        image.width,
                        image.height,
                    )

            self.vlist = self.program.vertex_list_indexed(
                int(
                    4 * (self.width // self.tile_size) * (self.height // self.tile_size)
                ),
                GL_TRIANGLES,
                indices,
                position=("f", position),
                tex_coords=("f", tex_coords),
            )
        self.program["translation"] = (self.x, self.y)
        self.program["scale"] = (self.scale_x, self.scale_y)
        self.program["color_add"] = (0, 0, 0)

        # self.program["center"] = center
        self.set_state_recursive()
        self.vlist.draw(GL_TRIANGLES)
        self.unset_state_recursive()

    def delete(self):
        if self.vlist:
            self.vlist.delete()
            self.vlist = None

    def __del__(self):
        if self.vlist:
            self.vlist.delete()
            self.vlist = None
