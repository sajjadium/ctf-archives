from functools import cache
from pathlib import Path
from typing import cast

import pyglet
from pyglet.image import ImageData, TextureGrid

import client


@cache
def get_ui_image() -> ImageData:
    return cast(
        ImageData,
        pyglet.image.load(Path(client.PATH, "assets/ui/16x16/Modern_UI_Style_1.png")),
    )


@cache
def get_ui_grid() -> TextureGrid:
    rows = 43
    columns = 61
    image_grid = pyglet.image.ImageGrid(get_ui_image(), rows=rows, columns=columns)
    texture_grid = image_grid.get_texture_sequence()
    # for some reason the grid is upside down, ouch
    texture_grid.items = [
        x
        for i in range(rows)
        for x in cast(list[int], texture_grid.items[i * columns :][:columns][::-1])
    ][::-1]
    return texture_grid
