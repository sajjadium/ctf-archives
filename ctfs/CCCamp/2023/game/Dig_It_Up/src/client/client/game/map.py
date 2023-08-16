from __future__ import annotations

import logging
import time
from asyncio import Lock, PriorityQueue
from copy import copy
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cache
from typing import TYPE_CHECKING, List, cast

from shared.constants import CHUNK_SIZE_X, CHUNK_SIZE_Y, TILE_SIZE_X, TILE_SIZE_Y
from shared.gen.messages.v1 import MapChunkResponse, TileCollision, Tileset

if TYPE_CHECKING:
    from client.scenes.game import Game

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
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.graphics.vertexdomain import IndexedVertexList
from pyglet.image import ImageData, Texture

import client
from client.game.camera import Camera
from client.game.utils import check_wait
from shared.map import Map, Tile

TEXTURE_SIZE = 16

TILES_PER_ROW = 16

TILE_IDS = [[0 for _ in range(CHUNK_SIZE_X)] for _ in range(CHUNK_SIZE_Y)]

TEX_COORDS: list[float] = [0.0] * (CHUNK_SIZE_X * CHUNK_SIZE_Y * 8)


VERTEX_SOURCE = """#version 330 core
    in vec2 tex_coords;
    in vec2 position;
    out vec2 vertex_colors;

    uniform vec2 translation;
    uniform bool center;

    uniform WindowBlock 
    {                       // This UBO is defined on Window creation, and available
        mat4 projection;    // in all Shaders. You can modify these matrixes with the
        mat4 view;          // Window.view and Window.projection properties.
    } window;

    mat4 m_translate = mat4(1.0);

    void main()
    {
        m_translate[3][0] = translation.x;
        m_translate[3][1] = -translation.y;
        gl_Position = window.projection * window.view * m_translate * vec4(position, 0, 1);
        vertex_colors = tex_coords;
    }
"""

FRAGMENT_SOURCE = """#version 330 core
    in vec2 vertex_colors;
    out vec4 final_color;
    uniform sampler2D texture_atlas;

    void main()
    {
        final_color = texture(texture_atlas, vertex_colors);
    }
"""


@cache
def get_map_shader() -> ShaderProgram:
    logging.debug("Map Shader Recalc")
    vert_shader = Shader(VERTEX_SOURCE, "vertex")
    frag_shader = Shader(FRAGMENT_SOURCE, "fragment")
    return ShaderProgram(vert_shader, frag_shader)


def get_vlist(program: ShaderProgram) -> IndexedVertexList:
    position: list[float] = []
    indices: list[int] = []
    tex_coords: list[float] = []
    for x in range(CHUNK_SIZE_X):
        for y in range(CHUNK_SIZE_Y):
            position += create_quad(x, y - CHUNK_SIZE_Y)
            indices += gen_quad_indices(CHUNK_SIZE_Y * y + x)
            tex_coords += [0] * 8

    return program.vertex_list_indexed(
        4 * CHUNK_SIZE_X * CHUNK_SIZE_Y,
        GL_TRIANGLES,
        indices,
        position=("f", position),
        tex_coords=("f", tex_coords),
    )  # type: ignore


def create_quad(
    x: float, y: float
) -> tuple[float, float, float, float, float, float, float, float]:
    x = x * TILE_SIZE_X
    y = y * TILE_SIZE_Y
    x2 = x + TILE_SIZE_X
    y2 = y + TILE_SIZE_Y
    return (x, y, x2, y, x2, y2, x, y2)


def create_quad_tex(
    offset: float, width: float, height: float
) -> tuple[float, float, float, float, float, float, float, float]:
    x = TEXTURE_SIZE * (offset % TILES_PER_ROW)
    y = TEXTURE_SIZE * (offset // TILES_PER_ROW)
    x2 = x + TEXTURE_SIZE
    y2 = y + TEXTURE_SIZE
    x /= width
    x2 /= width
    y /= height
    y2 /= height
    return (x, y2, x2, y2, x2, y, x, y)


def gen_quad_indices(n: int) -> tuple[int, int, int, int, int, int]:
    offset = n * 4
    return (0 + offset, 1 + offset, 2 + offset, 0 + offset, 2 + offset, 3 + offset)


@dataclass
class Chunk:
    tileset: Tileset
    width: int
    height: int
    tiles: List[List[int]]
    tex_coords: List[float]
    collisions: List[TileCollision]
    texture: Texture | None = None
    dirty: bool = True

    def get_texture(self):
        if self.texture:
            return self.texture
        self.texture = ImageData(
            self.tileset.width,
            self.tileset.height,
            "RGBA",
            self.tileset.tileset,
        ).get_texture()
        return self.texture


class ChunkWrapper:
    def __init__(self, cache: ChunkCache, item: MapChunkResponse) -> None:
        self.cache = cache
        self.value = item
        self.game = cast("Game", client.scene_manager.current_scene)

    def __f(self, val: MapChunkResponse):
        x, y = self.game.player.x, self.game.player.y
        return ((val.chunks[0].x + 0.5) * (CHUNK_SIZE_X * TILE_SIZE_X) - x) ** 2 + (
            (val.chunks[0].y + 0.5) * (CHUNK_SIZE_Y * TILE_SIZE_Y) - y
        ) ** 2

    def __lt__(self, obj: ChunkWrapper):
        return self.__f(self.value) < self.__f(obj.value)

    def __le__(self, obj: ChunkWrapper):
        return self.__f(self.value) <= self.__f(obj.value)

    def __eq__(self, obj: object):
        match obj:
            case ChunkWrapper():
                return self.__f(self.value) == self.__f(obj.value)
            case _:
                return False

    def __ne__(self, obj: object):
        match obj:
            case ChunkWrapper():
                return self.__f(self.value) != self.__f(obj.value)
            case _:
                return True

    def __gt__(self, obj: ChunkWrapper):
        return self.__f(self.value) > self.__f(obj.value)

    def __ge__(self, obj: ChunkWrapper):
        return self.__f(self.value) >= self.__f(obj.value)


class ChunkCache(dict[tuple[int, int], List[Chunk]]):
    request_time: dict[tuple[int, int], datetime]

    def __init__(self) -> None:
        self.request_time = dict()
        client.global_connection.map_chunk_handler += self._add_chunk_prio
        self.prio_queue: PriorityQueue[ChunkWrapper] = PriorityQueue()

    @staticmethod
    def _create_tex(tids: list[list[int]], tileset: Tileset) -> List[float]:
        # this is now really performant
        width = tileset.width
        height = tileset.height
        tex_coords: list[float] = copy(TEX_COORDS)
        for x_ in range(CHUNK_SIZE_X):
            for y_ in range(CHUNK_SIZE_Y):
                offset = tids[x_][y_]
                x = TEXTURE_SIZE * (offset % TILES_PER_ROW)
                y = TEXTURE_SIZE * (offset // TILES_PER_ROW)
                x2 = x + TEXTURE_SIZE
                y2 = y + TEXTURE_SIZE
                x /= width
                x2 /= width
                y /= height
                y2 /= height
                idx = (x_ * CHUNK_SIZE_Y + y_) * 8
                tex_coords[idx + 0] = x
                tex_coords[idx + 1] = y2
                tex_coords[idx + 2] = x2
                tex_coords[idx + 3] = y2
                tex_coords[idx + 4] = x2
                tex_coords[idx + 5] = y
                tex_coords[idx + 6] = x
                tex_coords[idx + 7] = y
        return tex_coords

    async def _add_chunk_prio(
        self, lock: Lock, chunk_response: MapChunkResponse
    ) -> None:
        cx = chunk_response.chunks[0].x
        cy = chunk_response.chunks[0].y

        print(
            "Adding chunk to QUEUE",
            cx,
            cy,
            len(chunk_response.chunks),
        )
        self.prio_queue.put_nowait(ChunkWrapper(self, chunk_response))
        async with lock:  # type: ignore
            while not self.prio_queue.empty():
                item = await self.prio_queue.get()
                await self._add_chunk(item.value)

    async def _add_chunk(self, chunk_response: MapChunkResponse) -> None:
        cx = chunk_response.chunks[0].x
        cy = chunk_response.chunks[0].y
        print(
            "Adding chunk",
            cx,
            cy,
            len(chunk_response.chunks),
        )
        chunks: List[Chunk] = []
        t0 = time.time()
        for c in chunk_response.chunks:
            tids = copy(TILE_IDS)
            for x in range(len(TILE_IDS)):
                tids[x] = copy(TILE_IDS[x])
                await check_wait()
            x = 0
            y = 0

            for tile in c.tiles:
                await check_wait()
                tids[x][CHUNK_SIZE_Y - 1 - y] = tile
                x += 1
                if x == c.width:
                    x = 0
                    y += 1

            tex_coords = self._create_tex(tids, c.tileset)

            cchunk = Chunk(
                c.tileset,
                c.width,
                c.height,
                tids,
                tex_coords,
                c.collisions,
            )

            chunks.append(cchunk)
        print("adding chunk took:", time.time() - t0)
        self.__setitem__((cx, cy), chunks)

    def __missing__(self, keys: tuple[int, int]) -> None:
        assert isinstance(keys, tuple) and len(keys) == 2

        if (
            keys not in self.request_time
            or self.request_time[keys] + timedelta(seconds=60) < datetime.now()
        ):
            print("Requesting chunk", keys[0], keys[1])
            self.request_time[keys] = datetime.now()
            client.global_connection.get_chunks(x=keys[0], y=keys[1])

        return None


class RenderChunk:
    chunk: None | tuple[int, int]

    def __init__(self) -> None:
        self.layers: List[IndexedVertexList] = []
        self.chunk = None

    def get_layer(self, idx: int, program: ShaderProgram) -> IndexedVertexList:
        if len(self.layers) <= idx:
            self.layers.append(get_vlist(program))
        return self.layers[idx]


class ClientMap(Map):
    program: ShaderProgram | None
    chunk_cache: ChunkCache

    def __init__(self):
        self.chunk_cache = ChunkCache()
        self.program = None
        self.vlists = None

    def get_tiles(
        self, x: float, y: float, user_id: str = ""
    ) -> tuple[List[Tile], float, float] | None:
        tiles: List[Tile] = []

        chunk_x = int(x // (CHUNK_SIZE_X * TILE_SIZE_X))
        chunk_y = int(y // (CHUNK_SIZE_Y * TILE_SIZE_Y))
        tile_x = int((x // TILE_SIZE_X) % CHUNK_SIZE_X)
        tile_y = int((-y // TILE_SIZE_Y) % CHUNK_SIZE_Y)

        chunks = self.chunk_cache[(chunk_x, chunk_y)]

        if not chunks:
            return ([], chunk_x + tile_x, chunk_y + tile_y)

        for chunk in chunks:
            tid = chunk.tiles[tile_x][tile_y]
            collision = chunk.collisions[tid]
            tiles.append(Tile(tid, collision.polygons))

        return (
            tiles,
            chunk_x * CHUNK_SIZE_X * TILE_SIZE_X + tile_x * TILE_SIZE_X,
            chunk_y * CHUNK_SIZE_Y * TILE_SIZE_Y
            + (-tile_y + CHUNK_SIZE_Y) * TILE_SIZE_Y,
        )

    def set_state(self) -> None:
        assert self.program
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.program.use()
        # self.texture.bind(self.texture_unit)
        # TODO restore state
        # glActiveTexture(GL_TEXTURE0 + self.texture_unit)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self) -> None:
        assert self.program
        self.program.stop()
        # glActiveTexture(GL_TEXTURE0 + self.texture_unit)
        # glBindTexture(GL_TEXTURE_2D, 0)
        # glActiveTexture(GL_TEXTURE0)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glDisable(GL_BLEND)

    def draw(self, camera: Camera) -> None:
        # render this chunk and all existing neighbour chunks
        chunk_x = int(camera.offset_x // (CHUNK_SIZE_X * TILE_SIZE_X))
        chunk_y = int(camera.offset_y // (CHUNK_SIZE_Y * TILE_SIZE_Y))
        if self.program is None:
            self.program = get_map_shader()
        if self.vlists is None:
            self.vlists = (*(RenderChunk() for _ in range(3 * 3)),)

        self.set_state()

        for x, y in [
            (0, 0),
            (0, 1),
            (0, -1),
            (-1, 0),
            (1, 0),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]:
            chunks = self.chunk_cache[(chunk_x + x, chunk_y + y)]

            if not chunks:
                continue

            idx = ((chunk_x + x + 1) % 3) * 3 + ((chunk_y + y + 1) % 3)
            render_chunk = self.vlists[idx]

            dirty = render_chunk.chunk != (chunk_x + x, chunk_y + y)

            for i, chunk in enumerate(chunks):
                vlist = render_chunk.get_layer(i, self.program)

                # TODO translate chunk
                self.program["translation"] = (
                    (chunk_x + x) * (CHUNK_SIZE_X * TILE_SIZE_X),
                    (chunk_y + y) * (CHUNK_SIZE_Y * TILE_SIZE_Y),
                )
                if dirty or chunk.dirty:
                    vlist.set_attribute_data("tex_coords", chunk.tex_coords)
                    chunk.dirty = False

                chunk.get_texture().bind(0)

                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

                vlist.draw(GL_TRIANGLES)
            render_chunk.chunk = (chunk_x + x, chunk_y + y)

        self.unset_state()
