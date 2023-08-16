from __future__ import annotations

import logging
from functools import cache
from pathlib import Path
from typing import Any, Dict, List, Tuple, cast

import numpy as np
import pytiled_parser
from mazelib import Maze
from mazelib.generate.DungeonRooms import DungeonRooms
from PIL import Image
from pytiled_parser import ObjectLayer, TileLayer, tiled_object
from pytiled_parser.common_types import OrderedPair

import server
from server.game.entity.area import AreaObject, DigArea
from server.game.entity.enemy import BossPatrolEnemy, Enemy, PatrolEnemy
from server.game.entity.npc import NPC, Interaction
from server.game.entity.object import Object
from server.game.entity.pickupable import Pickupable
from server.game.map.properties import NPC as PropertyNpc
from server.game.map.properties import AreaObject as PropertyAreaObject
from server.game.map.properties import CustomInteraction, CustomLayerType
from server.game.map.properties import Enemy as PropertyEnemy
from server.game.map.properties import Interaction as PropertyInteraction
from server.game.map.properties import Layer as PropertyLayer
from server.game.map.properties import Maze as PropertyMaze
from server.game.map.properties import MazeTileType
from server.game.map.properties import PatrolEnemy as PropertyPatrolEnemy
from server.game.map.properties import Pickupable as PropertyPickupable
from server.game.map.properties import Tile as PropertyTile
from server.game.map.properties import parse_additional_activities
from server.models import Session
from shared.constants import (
    CHUNK_SIZE_X,
    CHUNK_SIZE_Y,
    NUM_TILES_PER_COLUM,
    TILE_SIZE_X,
    TILE_SIZE_Y,
)
from shared.gen.messages.v1 import (
    Activity,
    Animation,
    AnimationStep,
    Direction,
    EntityAsset,
    EntityAssets,
    Item,
    MapChunk,
    MapChunkResponse,
    Point,
    Polygon,
    ServerMessage,
    TileCollision,
    Tileset,
)
from shared.map import Map as SharedMap
from shared.map import Tile


class Map(SharedMap):
    player_asset: EntityAssets
    objects: Dict[str, Object]

    def __init__(self, map_file: Path) -> None:
        self.map = pytiled_parser.parse_map(map_file)
        assert self.map.infinite, "Map in not inifite. Wrong map loaded?"

    def initialize(self):
        logging.debug(
            f"[Map] Loading map with size: {self.map.map_size} Tile size: {self.map.tile_size}"
        )

        self._parse_player()

        objs = self._parse_objects()

        self._preload_chunks()

        for tileset in self.map.tilesets.values():
            if tileset.name == "LLB-LandTileset":
                self.llb_tileset = tileset
            if tileset.name == "Colors":
                self.colors = tileset
            if tileset.name == "Maze":
                self.maze_tileset = tileset

        # assert self.llb_tileset, 'No tileset "CB-LandTileset" found.'
        # assert self.colors, 'No tileset "Colors" found.'
        # assert self.maze_tileset, 'No tileset "Maze" found.'

        return objs

    def _preload_chunks(self) -> None:
        for x, y in set(
            (
                [
                    (c.coordinates.x // CHUNK_SIZE_X, c.coordinates.y // CHUNK_SIZE_Y)
                    for l in self.map.layers
                    if isinstance(l, TileLayer) and l.chunks
                    for c in l.chunks
                ]
            )
        ):
            self.get_chunks(x, y, "")

    def _parse_player(self) -> None:
        for tileset in self.map.tilesets.values():
            if tileset.name != "player":
                continue

            if tileset.tiles is None:
                continue

            tile_ids = [k + tileset.firstgid for k in tileset.tiles.keys()]

            self.player_asset = self.get_entity_assets(tileset, tile_ids=tile_ids)

    def _parse_polygon_by_id(
        self, layer: ObjectLayer, polygon_id: int
    ) -> Polygon | None:
        polygon = next(
            (o for o in layer.tiled_objects if o.id == polygon_id),
            None,
        )
        if polygon is None:
            return None
        coll = self._parse_form(polygon)[0]
        return Polygon(points=[Point(x=p[0], y=p[1]) for p in coll])

    def _parse_objects(self) -> Dict[str, Object]:
        objs: Dict[str, Object] = {}
        for layer in self.map.layers:
            if not isinstance(layer, ObjectLayer):
                continue

            if layer.draw_order != "topdown":
                continue
            entity_assets = None
            for t in layer.tiled_objects:
                match t:
                    case tiled_object.Tile():
                        tileset_id = self._find_tileset_id(t.gid)

                        if tileset_id is None:
                            continue

                        tileset = self.map.tilesets[tileset_id]
                        tile_ids = set([t.gid])
                        additional_activities = parse_additional_activities(
                            t.properties
                        )

                        if tileset.tiles:
                            root_tile = tileset.tiles.get(t.gid - tileset_id, None)

                            if (
                                root_tile
                                and root_tile.class_ == "Tile"
                                and root_tile.properties
                            ):
                                root_tile_properties = PropertyTile().from_dict(
                                    root_tile.properties
                                )

                                for tile in tileset.tiles.values():
                                    if tile.id == t.gid:
                                        continue

                                    if tile.class_ != "Tile":
                                        continue

                                    properties = tile.properties
                                    if properties:
                                        properties = PropertyTile().from_dict(
                                            properties
                                        )

                                        if (
                                            properties.activity
                                            == root_tile_properties.activity
                                            or properties.activity
                                            in additional_activities
                                        ):
                                            tile_ids.add(tile.id + tileset_id)

                        entity_assets = self.get_entity_assets(tileset, list(tile_ids))
                    case tiled_object.Point():
                        pass
                    case _:
                        continue

                properties = t.properties
                coords = t.coordinates

                match t.class_:
                    case "Npc":
                        assert entity_assets
                        interactions: List[Interaction] = []

                        i = 0
                        while True:
                            key = f"interaction_{i}"

                            i += 1
                            if key not in properties:
                                break

                            interaction_properties = PropertyInteraction().from_dict(
                                properties[key]  # type: ignore
                            )

                            path = None
                            if interaction_properties.path != -1:
                                path_id = interaction_properties.path

                                path = self._parse_polygon_by_id(
                                    layer=layer, polygon_id=path_id
                                )

                            interactions.append(
                                Interaction(
                                    id=i,
                                    text=interaction_properties.text,
                                    path=path,
                                    speed=interaction_properties.speed,
                                    loop=interaction_properties.loop,
                                    next_interaction=interaction_properties.next_interaction,
                                    custom_interaction=interaction_properties.custom_interaction,
                                    custom_attribute=interaction_properties.custom_attribute,
                                )
                            )

                        npc_properties = PropertyNpc().from_dict(properties)

                        o = NPC(
                            x=coords.x,
                            y=coords.y,
                            direction=0,  # TODO: make direction right
                            entity_assets=entity_assets,
                            name=t.name,
                            interactable=npc_properties.interactable,
                            interact_distance=npc_properties.interact_distance,
                            interactions=interactions,
                        )
                    case "Enemy":
                        assert entity_assets

                        enemy_properties = PropertyEnemy().from_dict(properties)

                        o = Enemy(
                            x=coords.x,
                            y=coords.y,
                            direction=0,  # TODO: make direction right
                            entity_assets=entity_assets,
                            name=t.name,
                            health=enemy_properties.health,
                            health_max=enemy_properties.max_health,
                            speed=enemy_properties.speed,
                        )

                    case "PatrolEnemy":
                        assert entity_assets
                        enemy_properties = PropertyPatrolEnemy().from_dict(properties)

                        path = None
                        if enemy_properties.patrol_path != -1:
                            path_id = enemy_properties.patrol_path

                            path = self._parse_polygon_by_id(
                                layer=layer, polygon_id=path_id
                            )

                        o = PatrolEnemy(
                            path=path,
                            speed=enemy_properties.speed,
                            x=coords.x,
                            y=coords.y,
                            direction=0,  # TODO: make direction right
                            entity_assets=entity_assets,
                            name=t.name,
                            health=enemy_properties.health,
                            health_max=enemy_properties.max_health,
                        )

                    case "BossPatrolEnemy":
                        assert entity_assets
                        enemy_properties = PropertyPatrolEnemy().from_dict(properties)

                        path = None
                        if enemy_properties.patrol_path != -1:
                            path_id = enemy_properties.patrol_path

                            path = self._parse_polygon_by_id(
                                layer=layer, polygon_id=path_id
                            )

                        o = BossPatrolEnemy(
                            path=path,
                            speed=enemy_properties.speed,
                            x=coords.x,
                            y=coords.y,
                            direction=0,  # TODO: make direction right
                            entity_assets=entity_assets,
                            name=t.name,
                            health=enemy_properties.health,
                            health_max=enemy_properties.max_health,
                        )
                        print("Added BossPatrolEnemy")
                    case "Areaobject":
                        area_properties = PropertyAreaObject().from_dict(properties)

                        path = None
                        if area_properties.area != -1:
                            area_id = area_properties.area

                            path = self._parse_polygon_by_id(
                                layer=layer, polygon_id=area_id
                            )
                        assert path

                        match area_properties.interaction.custom_interaction:
                            case CustomInteraction.DIG:
                                o = DigArea(
                                    area=path,
                                    interaction=area_properties.interaction,
                                    interaction_on=area_properties.interaction_on,
                                    name="area",
                                    x=coords.x,
                                    y=coords.y,
                                    direction=0,
                                )
                            case _:
                                o = AreaObject(
                                    area=path,
                                    interaction=area_properties.interaction,
                                    interaction_on=area_properties.interaction_on,
                                    name="area",
                                    x=coords.x,
                                    y=coords.y,
                                    direction=0,
                                )

                    case "Pickupable":
                        pickupable_properties = PropertyPickupable().from_dict(
                            properties
                        )

                        item = Item(
                            description=pickupable_properties.description,
                            icon=pickupable_properties.icon,
                            name=t.name,
                            quantity=pickupable_properties.quantity,
                        )

                        o = Pickupable(
                            x=coords.x,
                            y=coords.y,
                            item=item,
                            name=t.name,
                            direction=0,
                            for_everyone=False,
                            garbage_collect_on_pickup=False,
                        )
                    case _:
                        o = Object(
                            x=coords.x,
                            y=coords.y,
                            direction=0,  # TODO: make direction right
                            name=t.name,
                        )

                objs[o.uuid] = o
        return objs

    def get_entity_assets(
        self, tileset: pytiled_parser.tileset.Tileset, tile_ids: List[int]
    ) -> EntityAssets:
        entity_asset = EntityAssets(
            height=tileset.tile_height,
            width=tileset.tile_width,
        )

        logging.debug(
            f"Getting tileset for ids: {str(tile_ids)} Tileset: {str(tileset)} Width: {tileset.tile_width} "
        )

        tileset_, new_tile_mapping, collisions = self.get_tileset(
            tileset.tile_width, tileset.tile_height, tile_ids
        )
        entity_asset.tileset = tileset_

        if tileset.tiles is None:
            return entity_asset

        for tile in tileset.tiles.values():
            if tile.id + tileset.firstgid not in tile_ids:
                continue

            properties = tile.properties

            if properties is None:
                properties = {}

            properties = PropertyTile.from_dict(properties)

            entity_asset.entity_assets.append(
                EntityAsset(
                    id=new_tile_mapping[tile.id + tileset.firstgid],
                    activity=Activity[f"ACTIVITY_{properties.activity.name}"],
                    direction=Direction[f"DIRECTION_{properties.direction.name}"],
                )
            )

        for tile_col in collisions:
            tile_collision = TileCollision(polygons=[])
            for col in tile_col:
                if col:
                    tile_collision.polygons.append(
                        Polygon(points=[Point(x=p[0], y=p[1]) for p in col])
                    )
            entity_asset.collisions.append(tile_collision)

        return entity_asset

    @cache
    def get_tileset_image(self, id: int) -> Image.Image:
        tileset = self.map.tilesets[id]
        tileset_png = Image.open(Path(server.PATH, f"./map/{tileset.image}"))  # type: ignore

        return tileset_png  # type: ignore

    def _create_tileset_image(
        self, rows: int, cols: int, tile_width: int, tile_height: int
    ) -> Image.Image:
        return Image.new("RGBA", (rows * tile_width, cols * tile_height))

    def _find_tileset_id(self, tile_id: int) -> int | None:
        gids = list(self.map.tilesets.keys())
        gids.sort(reverse=True)

        return next((gid for gid in gids if gid <= tile_id), None)

    def _parse_form(
        self, form: tiled_object.TiledObject
    ) -> List[List[Tuple[float, float]]]:
        coll: List[List[Tuple[float, float]]] = []

        match form:
            case tiled_object.Polygon():
                assert form.rotation == 0
                origin = form.coordinates
                points = [(p.x + origin.x, p.y + origin.y) for p in form.points]
                coll.append(points)
            case tiled_object.Rectangle():
                assert form.rotation == 0
                origin = form.coordinates
                points = [
                    (p.x + origin.x, p.y + origin.y)
                    for p in [
                        OrderedPair(0, 0),
                        OrderedPair(0, form.size.height),
                        OrderedPair(
                            form.size.width,
                            form.size.height,
                        ),
                        OrderedPair(form.size.width, 0),
                    ]
                ]
                coll.append(points)
            case _:
                logging.warning("Unknown object", form)

        return coll

    def get_tileset(
        self, tile_width: int, tile_height: int, tile_ids: List[int]
    ) -> Tuple[Tileset, Dict[int, int], List[List[List[Tuple[float, float]]]]]:
        old_id_mapping: Dict[int, int] = {}

        result_tileset = Tileset()
        result_image = self._create_tileset_image(
            NUM_TILES_PER_COLUM, 1, tile_width, tile_height
        )

        tile_collisions: List[List[List[Tuple[float, float]]]] = []

        for tile_id in tile_ids:
            new_tile_index = len(old_id_mapping)

            if new_tile_index != 0 and new_tile_index % NUM_TILES_PER_COLUM == 0:
                tmp_image = result_image
                result_image = self._create_tileset_image(
                    NUM_TILES_PER_COLUM,
                    (new_tile_index // NUM_TILES_PER_COLUM) + 1,
                    tile_width,
                    tile_height,
                )
                result_image.paste(tmp_image)

            coll: List[List[Tuple[float, float]]] = []

            tileset_id = self._find_tileset_id(tile_id=tile_id)
            if tileset_id is not None:
                tileset = self.map.tilesets[tileset_id]
                tileset_image = self.get_tileset_image(tileset_id)

                local_id = tile_id - tileset.firstgid

                if tileset.tiles is not None and local_id in tileset.tiles:
                    tile = tileset.tiles[local_id]

                    if tile.animation is not None:
                        animation = Animation(id=tile_id)

                        for frame in tile.animation:
                            t_id = frame.tile_id + tileset.firstgid
                            animation.animation_setps.append(
                                AnimationStep(id=t_id, duration=frame.duration)
                            )

                            if t_id not in tile_ids:
                                tile_ids.append(t_id)

                        result_tileset.animations.append(animation)

                    match tile.objects:
                        case pytiled_parser.layer.ObjectLayer() as object_layer:
                            for collision_object in object_layer.tiled_objects:
                                coll += self._parse_form(collision_object)
                        case _:
                            pass

                assert (
                    tileset.tile_width == tile_width
                    and tileset.tile_height == tile_height
                ), f"Tiles have to be the same size! {tileset.name} {tileset.tile_width} != {tile_width} or {tileset.tile_height} != {tile_height}"

                x_start = (local_id % tileset.columns) * tileset.tile_width
                y_start = (local_id // tileset.columns) * tileset.tile_height
                x_end = x_start + tileset.tile_width
                y_end = y_start + tileset.tile_height

                new_tile_x = (new_tile_index % NUM_TILES_PER_COLUM) * tileset.tile_width
                new_tile_y = (
                    new_tile_index // NUM_TILES_PER_COLUM
                ) * tileset.tile_height

                # Crop tile from the global tileset to the local tileset
                result_image.paste(
                    tileset_image.crop((x_start, y_start, x_end, y_end)),
                    (new_tile_x, new_tile_y),
                )

            tile_collisions.append(coll)

            old_id_mapping[tile_id] = new_tile_index

        for animation in result_tileset.animations:
            animation.id = old_id_mapping[animation.id]

            for step in animation.animation_setps:
                step.id = old_id_mapping[step.id]

        img_byte_arr = result_image.tobytes()
        result_tileset.tileset = img_byte_arr
        result_tileset.width = result_image.width
        result_tileset.height = result_image.height

        return result_tileset, old_id_mapping, tile_collisions

    # Gets a new tileset for a given chunk
    # Returns a tuple of:
    # - the new tileset as raw image bytes
    # - the tile mapping of old to new tile ids

    def get_tileset_for_chunk(
        self, chunk: pytiled_parser.layer.Chunk
    ) -> Tuple[Tileset, Dict[int, int], List[List[List[Tuple[float, float]]]]]:
        gids = list(self.map.tilesets.keys())
        gids.sort(reverse=True)

        # Get number of unique tiles to estimate result tilset size
        unique_tiles: List[int] = []
        for row in chunk.data:
            for col in row:
                if not col in unique_tiles:
                    unique_tiles.append(col)

        num_unique_tiles = len(unique_tiles)
        logging.debug(f"Number of unique tiles in chunk: {num_unique_tiles}")

        return self.get_tileset(TILE_SIZE_X, TILE_SIZE_Y, unique_tiles)

    def get_tile_layers(
        self, layers: List[pytiled_parser.Layer]
    ) -> List[pytiled_parser.TileLayer]:
        layers_ret: List[pytiled_parser.TileLayer] = []

        for layer in layers:
            if isinstance(layer, pytiled_parser.TileLayer):
                layers_ret.append(layer)

            if isinstance(layer, pytiled_parser.LayerGroup):
                if layer.layers:
                    layers_ret += self.get_tile_layers(layer.layers)

        return layers_ret

    def is_dynamic_chunk(self, x: float, y: float) -> bool:
        for layer in self.get_tile_layers(self.map.layers):
            if layer.properties:
                properties = PropertyLayer().from_dict(layer.properties)

                if properties.type != CustomLayerType.DYNAMIC:
                    continue
            else:
                continue

            match layer.chunks:
                case None:
                    continue
                case chunks:
                    pass

            # Find the chunk the client requested
            chunk = next(
                (
                    item
                    for item in chunks
                    if (
                        item.coordinates.x == x * CHUNK_SIZE_X
                        and item.coordinates.y == y * CHUNK_SIZE_Y
                    )
                ),
                None,
            )

            if chunk:
                return True

        return False

    def get_chunks(self, x: float, y: float, user_id: str) -> List[MapChunk]:
        if self.is_dynamic_chunk(x=x, y=y):
            return self.get_dynamic_chunk(
                requested_chunk_block_x=x, requested_chunk_block_y=y, user_id=user_id
            )
        else:
            return self.get_static_chunks(x=x, y=y)

    def _get_neighbouring_chunks(
        self,
        start: pytiled_parser.Chunk,
        chunks: List[pytiled_parser.Chunk],
        visited: List[pytiled_parser.Chunk],
    ) -> None:
        queue: List[pytiled_parser.Chunk] = [start]

        while len(queue) > 0:
            current = queue.pop()
            visited.append(current)

            for x, y in [
                (0, 1),
                (0, -1),
                (-1, 0),
                (1, 0),
            ]:
                chunk = next(
                    (
                        item
                        for item in chunks
                        if (
                            item.coordinates.x
                            == current.coordinates.x + x * CHUNK_SIZE_X
                            and item.coordinates.y
                            == current.coordinates.y + y * CHUNK_SIZE_Y
                            and item not in visited
                            and item not in queue
                        )
                    ),
                    None,
                )

                if chunk:
                    queue.append(chunk)

    def get_dynamic_chunk(
        self,
        requested_chunk_block_x: float,
        requested_chunk_block_y: float,
        user_id: str,
    ) -> List[MapChunk]:
        if user_id == "":
            return []

        session = server.game_state.user_sessions[user_id]

        if len(session.maze) == 0:
            for layer in self.get_tile_layers(self.map.layers):
                if layer.properties:
                    properties = PropertyLayer().from_dict(layer.properties)

                    if properties.type != CustomLayerType.DYNAMIC:
                        continue
                else:
                    continue

                match layer.chunks:
                    case None:
                        continue
                    case chunks:
                        pass

                # Find the chunk the client requested
                chunk = next(
                    (
                        item
                        for item in chunks
                        if (
                            item.coordinates.x == requested_chunk_block_x * CHUNK_SIZE_X
                            and item.coordinates.y
                            == requested_chunk_block_y * CHUNK_SIZE_Y
                        )
                    ),
                    None,
                )

                if not chunk:
                    continue

                if len(session.waiting_maze_chunks) == 0:
                    maze_future = server.executor.submit(
                        self.generate_maze, chunk, chunks
                    )

                    maze_future.add_done_callback(
                        lambda res: self.generate_maze_result(session, res.result())
                    )

                session.waiting_maze_chunks.append(
                    (int(chunk.coordinates.x), int(chunk.coordinates.y))
                )

                data = np.full(
                    shape=(32, 32), fill_value=self.maze_tileset.firstgid + 8
                )

                c = pytiled_parser.Chunk(
                    coordinates=pytiled_parser.OrderedPair(
                        x=int(chunk.coordinates.x),
                        y=int(chunk.coordinates.y),
                    ),
                    size=pytiled_parser.Size(CHUNK_SIZE_X, CHUNK_SIZE_Y),
                    data=data.tolist(),
                )

                chunk = self._get_chunk(chunk=c)

                return [chunk]

        c = next(
            (
                c
                for c in session.maze
                if c[0].x == requested_chunk_block_x
                and c[0].y == requested_chunk_block_y
            ),
            None,
        )
        if c:
            return c
        else:
            return []

    def generate_maze_result(
        self, session: Session, maze: list[list[MapChunk]]
    ) -> None:
        session.maze = maze

        for x, y in session.waiting_maze_chunks:
            c = next(
                (
                    c
                    for c in session.maze
                    if c[0].x == x // CHUNK_SIZE_X and c[0].y == y // CHUNK_SIZE_Y
                ),
                None,
            )

            if c is None:
                continue

            server.global_server.broadcast_sync(
                message=ServerMessage(chunk=MapChunkResponse(chunks=c)),
                include=[session.peer],
            )

        session.waiting_maze_chunks.clear()

    def generate_maze(
        self, chunk: pytiled_parser.Chunk, chunks: List[pytiled_parser.Chunk]
    ) -> list[list[MapChunk]]:
        all_chunks: List[List[MapChunk]] = []

        chunk_block: list[pytiled_parser.Chunk] = []
        self._get_neighbouring_chunks(chunk, chunks, chunk_block)
        x_coordinates = [c.coordinates.x for c in chunk_block]
        y_coordinates = [c.coordinates.y for c in chunk_block]

        width = abs(max(x_coordinates) - min(x_coordinates)) + CHUNK_SIZE_X
        height = abs(max(y_coordinates) - min(y_coordinates)) + CHUNK_SIZE_Y
        chunk_block_x = min(x_coordinates)
        chunk_block_y = min(y_coordinates)

        assert (width // CHUNK_SIZE_X) * (height // CHUNK_SIZE_Y) == len(
            chunk_block
        ), "Maze has to be in a rectangle!"

        start_end: list[tuple[int, int]] = []

        for c in chunk_block:
            for y, row in enumerate(c.data):
                for x, tile_id in enumerate(row):
                    tileset_id = self._find_tileset_id(tile_id)

                    if not tileset_id:
                        continue

                    tileset = self.map.tilesets[tileset_id]
                    if not tileset.tiles:
                        continue

                    tile = tileset.tiles[tile_id - tileset.firstgid]

                    if not tile.properties:
                        continue

                    properties = PropertyMaze().from_dict(tile.properties)
                    if properties.type == MazeTileType.START_END:
                        mx = (c.coordinates.x + x) - chunk_block_x + 1
                        my = (c.coordinates.y + y) - chunk_block_y
                        # account for odd size and room size
                        if mx == width:
                            mx -= 2
                        if my == height:
                            my -= 2
                        start_end.append(
                            (
                                int(mx // 3),
                                int(my // 3),
                            )
                        )

        assert (
            len(start_end) == 2
        ), f"There must be 2 Start/Ends but there are {len(start_end)}"

        maze = Maze()
        maze.generator = DungeonRooms(  # type: ignore
            (width // 3 - 1) // 2,
            (height // 3 - 1) // 2,
            [
                [
                    a,
                    (
                        a[0] + 1,
                        a[1] + 1,
                    ),
                ]
                for a in start_end
            ],
        )

        maze.generate()

        if maze.grid is None:
            return all_chunks

        grid: Any = maze.grid.astype("int32")

        grid = np.repeat(a=grid, repeats=3, axis=0)
        grid = np.repeat(a=grid, repeats=3, axis=1)

        grid_shape = grid.shape
        grid_shape = (
            ((grid_shape[0] // CHUNK_SIZE_X) + 1) * CHUNK_SIZE_X - grid_shape[0],
            ((grid_shape[1] // CHUNK_SIZE_Y) + 1) * CHUNK_SIZE_Y - grid_shape[1],
        )
        grid = np.pad(
            array=grid,
            pad_width=((0, grid_shape[0]), (0, grid_shape[1])),
            constant_values=1,
        )

        grid = np.where(grid == 1, 0, 1)

        maze.grid = grid

        for s in start_end:
            y = s[0] * 3
            x = s[1] * 3
            if y == width - 3 - 1:
                for x_off in range(6):
                    grid[y + 3][x + x_off] = 1
            if x == height - 3 - 1:
                for y_off in range(6):
                    grid[y + y_off][x + 3] = 1

        maze.grid = grid

        x, y = grid, np.roll(grid, 1, 0)
        y[0] = 0
        coll_n = np.where(x & y == 1, 2, 0)

        x, y = grid, np.roll(grid, -1, 0)
        y[-1] = 0
        coll_s = np.where(x & y == 1, 8, 0)

        x, y = grid, np.roll(grid, 1, 1)
        y[:, 0] = 0
        coll_e = np.where(x & y == 1, 4, 0)

        x, y = grid, np.roll(grid, -1, 1)
        y[:, -1] = 0
        coll_w = np.where(x & y == 1, 16, 0)

        x, y = grid, np.roll(grid, 1, 0)
        y[0] = 0
        x, y = x, np.roll(y, 1, 1)
        y[:, 0] = 0
        coll_ne = np.where(x & y == 1, 32, 0)

        x, y = grid, np.roll(grid, -1, 0)
        y[-1] = 0
        x, y = x, np.roll(y, 1, 1)
        y[:, 0] = 0
        coll_se = np.where(x & y == 1, 64, 0)

        x, y = grid, np.roll(grid, -1, 0)
        y[-1] = 0
        x, y = x, np.roll(y, -1, 1)
        y[:, -1] = 0
        coll_sw = np.where(x & y == 1, 128, 0)

        x, y = grid, np.roll(grid, 1, 0)
        y[0] = 0
        x, y = x, np.roll(y, -1, 1)
        y[:, -1] = 0
        coll_nw = np.where(x & y == 1, 256, 0)

        grid = (
            grid
            + coll_n
            + coll_s
            + coll_e
            + coll_w
            + coll_ne
            + coll_se
            + coll_sw
            + coll_nw
        )

        quadrant_offset = self.llb_tileset.firstgid + 105

        valid = [
            0b000000000,
            0b000100111,
            0b001001101,
            0b001101111,
            0b010011001,
            0b011011101,
            0b011101111,
            0b011111101,
            0b011111111,
            0b100010011,
            0b100110111,
            0b101001101,
            0b101010011,
            0b101101111,
            0b101110111,
            0b101111111,
            0b110011011,
            0b110110111,
            0b110111011,
            0b110111111,
            0b111011011,
            0b111011101,
            0b111011111,
            0b000010101,
            0b000110101,
            0b000110111,
            0b001110101,
            0b001111111,
            0b010010101,
            0b010011101,
            0b101010111,
            0b101011101,
            0b110010101,
            0b110011111,
            0b000010001,
            0b010100111,
            0b010111001,
            0b100010101,
            0b100010111,
            0b110011111,
            0b111111111,
            0b100100111,
            0b100110011,
            0b110010011,
        ]

        print(
            "\n".join(
                f"unmapped tile: 0b{l:09b}"
                for l in cast(list[int], np.unique(grid).tolist())
                if l not in valid
            )
        )

        # Path
        grid[grid == 0b000000000] = quadrant_offset - 89

        grid[grid == 0b000100111] = quadrant_offset + 34
        grid[grid == 0b001001101] = quadrant_offset + 32
        grid[grid == 0b001101111] = quadrant_offset + 33
        grid[grid == 0b010011001] = quadrant_offset + 0
        grid[grid == 0b011011101] = quadrant_offset + 16
        grid[grid == 0b011101111] = quadrant_offset + 33
        grid[grid == 0b011111101] = quadrant_offset + 16
        grid[grid == 0b011111111] = quadrant_offset + 21
        grid[grid == 0b100010011] = quadrant_offset + 2
        grid[grid == 0b100110111] = quadrant_offset + 18
        grid[grid == 0b101001101] = quadrant_offset + 32
        grid[grid == 0b101010011] = quadrant_offset + 2
        grid[grid == 0b101101111] = quadrant_offset + 33
        grid[grid == 0b101110111] = quadrant_offset + 18
        grid[grid == 0b101111111] = quadrant_offset + 20
        grid[grid == 0b110011011] = quadrant_offset + 1
        grid[grid == 0b110110111] = quadrant_offset + 18
        grid[grid == 0b110111011] = quadrant_offset + 1
        grid[grid == 0b110111111] = quadrant_offset + 36
        grid[grid == 0b111011011] = quadrant_offset + 1
        grid[grid == 0b111011101] = quadrant_offset + 16
        grid[grid == 0b111011111] = quadrant_offset + 37

        grid[grid == 0b000010101] = quadrant_offset + 17
        grid[grid == 0b000110101] = quadrant_offset + 17
        grid[grid == 0b000110111] = quadrant_offset + 34
        grid[grid == 0b001110101] = self.colors.firstgid + 0
        grid[grid == 0b001111111] = self.colors.firstgid + 0
        grid[grid == 0b010010101] = self.colors.firstgid + 5
        grid[grid == 0b010011101] = self.colors.firstgid + 4
        grid[grid == 0b101010111] = self.colors.firstgid + 6
        grid[grid == 0b101011101] = self.colors.firstgid + 7
        grid[grid == 0b110010101] = self.colors.firstgid + 2
        grid[grid == 0b110011111] = quadrant_offset + 34
        grid[grid == 0b000010001] = self.colors.firstgid + 3
        grid[grid == 0b010100111] = quadrant_offset + 34
        grid[grid == 0b010111001] = quadrant_offset + 0
        grid[grid == 0b100010101] = quadrant_offset + 17
        grid[grid == 0b100010111] = quadrant_offset + 2
        grid[grid == 0b110011111] = self.colors.firstgid + 8

        grid[grid == 0b100100111] = self.colors.firstgid + 0
        grid[grid == 0b100110011] = self.colors.firstgid + 0
        grid[grid == 0b110010011] = self.colors.firstgid + 0

        # Middle Border
        grid[grid == 0b111111111] = quadrant_offset + 17

        # grid *= 17 - 1
        # grid += self.cave_tileset.firstgid + 1

        for s in start_end:
            y = s[0] * 3
            x = s[1] * 3
            if y == width - 3 - 1:
                for x_off in range(4):
                    grid[y + 3][x + 1 + x_off] = quadrant_offset + 17
                grid[y + 3][x] = quadrant_offset + 1
                grid[y + 3][x + 5] = quadrant_offset + 33
            if y == 0:
                for x_off in range(4):
                    grid[y][x + 1 + x_off] = quadrant_offset + 17
                grid[y][x] = quadrant_offset + 1
                grid[y][x + 5] = quadrant_offset + 33

        maze_rows: Any = np.split(
            ary=grid, indices_or_sections=int(width // CHUNK_SIZE_X)
        )
        maze_chunks = [
            np.split(ary=row, indices_or_sections=int(height // CHUNK_SIZE_Y), axis=1)
            for row in maze_rows
        ]

        for chunk_x, row in enumerate(maze_chunks):
            for chunk_y, ch in enumerate(row):
                c = pytiled_parser.Chunk(
                    coordinates=pytiled_parser.OrderedPair(
                        x=int(chunk_x * CHUNK_SIZE_X + chunk_block_x),
                        y=int(chunk_y * CHUNK_SIZE_Y + chunk_block_y),
                    ),
                    size=pytiled_parser.Size(CHUNK_SIZE_X, CHUNK_SIZE_Y),
                    data=ch.transpose().tolist(),
                )

                try:
                    ch = self._get_chunk(chunk=c)
                except Exception as e:
                    print(e)
                    continue

                all_chunks.append([ch])

        # session.maze = all_chunks

        return all_chunks

    # Chunks are not in absolute coordinates, but chunk coordinates
    # E.g. (x=0, y=0) is top left, (x=0,y=1) is right below the left top corner
    # Returns:
    # - a dictionary with x,y,width,height, tiles,tileset
    @cache
    def get_static_chunks(self, x: int, y: int) -> List[MapChunk]:
        all_chunks: List[MapChunk] = []

        for layer in self.get_tile_layers(self.map.layers):
            if layer.properties:
                properties = PropertyLayer().from_dict(layer.properties)

                if properties.type == CustomLayerType.DYNAMIC:
                    continue

            match layer.chunks:
                case None:
                    continue
                case chunks:
                    pass

            # Find the chunk the client requested
            chunk = next(
                (
                    item
                    for item in chunks
                    if (
                        item.coordinates.x == x * CHUNK_SIZE_X
                        and item.coordinates.y == y * CHUNK_SIZE_Y
                    )
                ),
                None,
            )

            if chunk is None:
                continue

            all_chunks.append(self._get_chunk(chunk=chunk))

        return all_chunks

    def _get_chunk(self, chunk: pytiled_parser.Chunk) -> MapChunk:
        ret = MapChunk(
            x=int(chunk.coordinates.x // CHUNK_SIZE_X),
            y=int(chunk.coordinates.y // CHUNK_SIZE_Y),
            width=CHUNK_SIZE_X,
            height=CHUNK_SIZE_Y,
        )

        # Render tileset of the chunk
        tileset, new_tile_mapping, collisions = self.get_tileset_for_chunk(chunk)

        # Get binary stream of tiles data, serialized to protobuf
        for row in chunk.data:
            for tile in row:
                ret.tiles.append(new_tile_mapping[tile])

        ret.tileset = tileset

        for tile_col in collisions:
            tile_collision = TileCollision(polygons=[])
            for col in tile_col:
                if col:
                    tile_collision.polygons.append(
                        Polygon(points=[Point(p[0], p[1]) for p in col])
                    )
            ret.collisions.append(tile_collision)

        return ret

    def get_tiles(
        self, x: float, y: float, user_id: str
    ) -> Tuple[List[Tile], float, float] | None:
        tiles: List[Tile] = []

        chunk_x = x // (CHUNK_SIZE_X * TILE_SIZE_X)
        chunk_y = y // (CHUNK_SIZE_Y * TILE_SIZE_Y)
        tile_x = int((x // TILE_SIZE_X) % CHUNK_SIZE_X)
        tile_y = int((-y // TILE_SIZE_Y) % CHUNK_SIZE_Y)

        chunks = self.get_chunks(chunk_x, chunk_y, user_id)

        if len(chunks) == 0:
            return None

        for chunk in chunks:
            tile_id = chunk.tiles[tile_x + (CHUNK_SIZE_Y - 1 - tile_y) * CHUNK_SIZE_X]
            tile = Tile(tile_id, chunk.collisions[tile_id].polygons)

            tiles.append((tile))

        return (
            tiles,
            chunk_x * CHUNK_SIZE_X * TILE_SIZE_X + tile_x * TILE_SIZE_X,
            chunk_y * CHUNK_SIZE_Y * TILE_SIZE_Y
            + (-tile_y + CHUNK_SIZE_Y) * TILE_SIZE_Y,
        )
