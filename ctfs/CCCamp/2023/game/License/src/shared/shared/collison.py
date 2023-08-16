import functools
import operator
from typing import Iterator, Tuple

import collision

from shared.gen.messages.v1 import Polygon
from shared.map import Map


def bb(x: float, y: float, w: float, h: float) -> Iterator[Tuple[float, float]]:
    yield x, y
    yield x + w, y
    yield x + w, y + h
    yield x, y + h


cached_polys: dict[int, collision.Concave_Poly] = {}


def to_poly(poly: Polygon) -> collision.Concave_Poly:
    id_ = id(poly)
    if id_ in cached_polys:
        return cached_polys[id_]

    p = collision.Concave_Poly(
        collision.Vector(0, 0),
        [collision.Vector(p.x, p.y) for p in poly.points],
    )
    cached_polys[id_] = p

    return p


def point_in_poly(x: float, y: float, poly: Polygon) -> bool:
    to_test = to_poly(poly=poly)
    return collision.point_in_poly(collision.Vector(x, y), to_test)


class CollisionManager:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    # handle different collision types so that we only cancel direction of collision
    def _do_edge_detection(
        self,
        map: Map,
        old_x: float,
        old_y: float,
        new_x: float,
        new_y: float,
        offset_x: int,
        offset_y: int,
        user_id: str,
    ) -> Tuple[float, float] | None:
        player = collision.Poly(
            collision.Vector(new_x, old_y),
            [
                collision.Vector(x, y)
                for x, y in [
                    (0, 0),
                    (0, self.height),
                    (self.width, self.height),
                    (self.width, 0),
                ]
            ],
        )
        player2 = collision.Poly(
            collision.Vector(old_x, new_y),
            [
                collision.Vector(x, y)
                for x, y in [
                    (0, 0),
                    (0, self.height),
                    (self.width, self.height),
                    (self.width, 0),
                ]
            ],
        )

        match map.get_tiles(new_x + offset_x, old_y + offset_y, user_id):
            case None:
                return
            case tiles, tx, ty:
                pass

        for col in functools.reduce(
            operator.iconcat, [tile.collision for tile in tiles], []
        ):
            poly = collision.Concave_Poly(
                collision.Vector(tx, ty),
                [collision.Vector(p.x, p.y) for p in col.points],
            )
            c = collision.collide(poly, player)
            if c:
                break
        else:
            return (new_x, old_y)

        match map.get_tiles(old_x + offset_x, new_y + offset_y, user_id):
            case None:
                return
            case tiles2, tx2, ty2:
                pass

        for col in functools.reduce(
            operator.iconcat, [tile.collision for tile in tiles2], []
        ):
            poly = collision.Concave_Poly(
                collision.Vector(tx2, ty2),
                [collision.Vector(p.x, p.y) for p in col.points],
            )
            c = collision.collide(poly, player2)
            if c:
                break
        else:
            return (old_x, new_y)

        return (old_x, old_y)

    def check_collisons(
        self,
        map: Map,
        old_x: float,
        old_y: float,
        new_x: float,
        new_y: float,
        user_id: str = "",
    ) -> Tuple[float, float] | None:
        entity = collision.Poly(
            collision.Vector(new_x, new_y),
            [
                collision.Vector(x, y)
                for x, y in [
                    (0, 0),
                    (0, self.height),
                    (self.width, self.height),
                    (self.width, 0),
                ]
            ],
        )

        colls: set[int] = set()
        for idx, (x, y) in enumerate(bb(new_x, new_y, self.width, -self.height)):
            match map.get_tiles(x=x, y=y, user_id=user_id):
                case None:
                    return None
                case tiles, tx, ty:
                    pass

            for tile in tiles:
                for col in tile.collision:
                    poly = collision.Concave_Poly(
                        collision.Vector(tx, ty),
                        [collision.Vector(p.x, p.y) for p in col.points],
                    )
                    resp = collision.Response()
                    c = collision.collide(poly, entity, resp)
                    if c:
                        colls.add(idx)

        match list(colls):
            case []:
                return (new_x, new_y)
            case [0, 1]:
                return (new_x, old_y)
            case [0, 3]:
                return (old_x, new_y)
            case [2, 3]:
                return (new_x, old_y)
            case [1, 2]:
                return (old_x, new_y)
            case [0]:
                return self._do_edge_detection(
                    map, old_x, old_y, new_x, new_y, 0, 0, user_id
                )
            case [1]:
                return self._do_edge_detection(
                    map, old_x, old_y, new_x, new_y, self.width, 0, user_id
                )
            case [2]:
                return self._do_edge_detection(
                    map, old_x, old_y, new_x, new_y, self.width, -self.height, user_id
                )
            case [3]:
                return self._do_edge_detection(
                    map, old_x, old_y, new_x, new_y, 0, -self.height, user_id
                )
            case _:
                pass

        return (old_x, old_y)
