
from typing import List, Tuple
from enum import Enum
import json
import itertools

import numpy as np
import pygame
from pygame import gfxdraw

from .constants import GRID_SIZE
from .anim import Animation, Transition, PlayerMoveAnimation, TreeFallAnimation, \
    TreeIntoWaterAnimation, TreeRollAnimation, MakeRaftAnimation, RaftAnimation
from .defs import LogOrientation, Tiles

LAND_COLOR = (23,32,52)
WATER_COLOR = (96,106,137)
PLAYER_COLOR = (255,255,255)
TREE_COLOR = (95,205,228)
STUMP_COLOR = (54,64,88)

PLAYER_SIZE = 0.3 # 0 (large) to 0.5 (small)
TREE_SIZE = 0.3


def _bound(x, a, b):
    return max(min(x, b), a)


class EntityManager(object):
    SIZE = 16

    buckets: List[List[List['Entity']]]
    width: int
    height: int
    bx: int
    by: int

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buckets = []
        self.bx = (width // EntityManager.SIZE) + 1
        self.by = (height // EntityManager.SIZE) + 1
        for y in range(self.by):
            b = []
            for x in range(self.bx):
                b.append([])
            self.buckets.append(b)

    def add(self, entity):
        by = entity.ly // EntityManager.SIZE
        bx = entity.lx // EntityManager.SIZE
        self.buckets[by][bx].append(entity)
        entity.em = self

    def update(self, entity, x, y, tx, ty):
        by = y // EntityManager.SIZE
        bx = x // EntityManager.SIZE
        self.buckets[by][bx].remove(entity)
        by = ty // EntityManager.SIZE
        bx = tx // EntityManager.SIZE
        self.buckets[by][bx].append(entity)

    def at(self, x, y):
        by = y // EntityManager.SIZE
        bx = x // EntityManager.SIZE
        return [ent for ent in self.buckets[by][bx] if ent.ly == y and ent.lx == x and ent.active]

    def in_bounds(self, tx, ty):
        for y in range(max(0, (ty[0] // EntityManager.SIZE) - 1), min(self.by - 1, (ty[1] // EntityManager.SIZE) + 1) + 1):
            for x in range(max(0, (tx[0] // EntityManager.SIZE) - 1), min(self.bx - 1, (tx[1] // EntityManager.SIZE) + 1) + 1):
                for e in self.buckets[y][x]:
                    yield e


class Player(object):
    lx: int
    ly: int
    x: float
    y: float

    def __init__(self, x, y):
        self.lx = x
        self.ly = y
        self.x = x
        self.y = y


class Entity(object):
    lx: int
    ly: int
    x: float
    y: float
    active: bool
    em: EntityManager

    def __init__(self, x, y):
        self.lx = x
        self.ly = y
        self.x = x
        self.y = y
        self.active = True

    def update(self, x, y, tx, ty):
        self.em.update(self, x, y, tx, ty)


class Log(Entity):
    orientation: LogOrientation
    fall_p: float
    is_raft: bool
    raft_partner: 'Log'

    def __init__(self, x, y):
        super(Log, self).__init__(x,y)
        self.orientation = LogOrientation.STANDING
        self.fall_p = 0

        self.is_raft = False
        self.raft_partner = None


class Map(object):
    width: int
    height: int
    dat: 'np.ndarray'
    em: EntityManager
    player: Player
    transition: Animation
    history: List[Animation]

    @staticmethod
    def load(file, px, py):
        try:
            m = np.load(file)
        except:
            print('Error loading map')
            exit(-1)

        width = m.shape[1]
        height = m.shape[0]

        wy, wx = np.where(m == 3)

        em = EntityManager(width, height)
        for y,x in zip(wy,wx):
            em.add(Log(x,y))

        return Map(width, height, m, em, Player(px, py))

    def __init__(self, width, height, dat, em, player):
        self.width = width
        self.height = height
        self.dat = dat
        self.em = em
        self.player = player
        self.transition = None
        self.history = []

    def _coords_to_screen(self, screen, x, y, camera):
        width, height = screen.get_size()
        nx = ((x - camera.x) * GRID_SIZE * camera.zoom) + (float(width) / 2)
        ny = ((y - camera.y) * GRID_SIZE * camera.zoom) + (float(height) / 2)
        nw = GRID_SIZE * camera.zoom
        return (nx,ny,nw)

    def render_base(self, screen, camera, bx, by):
        for y in range(*by):
            for x in range(*bx):
                nx, ny, nw = self._coords_to_screen(screen, x, y, camera)

                if self.dat[y][x] == Tiles.LAND:
                    pygame.draw.rect(
                        screen,
                        LAND_COLOR,
                        (nx, ny, int(nw+1), int(nw+1))
                    )
                elif self.dat[y][x] == Tiles.LAND_ROCK:
                    pygame.draw.rect(
                        screen,
                        LAND_COLOR,
                        (nx, ny, int(nw+1), int(nw+1))
                    )
                    pygame.draw.rect(
                        screen,
                        STUMP_COLOR,
                        (nx+(nw*0.2), ny+(nw*0.2), int((nw*0.6)+1), int((nw*0.6)+1))
                    )
                elif self.dat[y][x] == Tiles.STUMP:
                    pygame.draw.rect(
                        screen,
                        LAND_COLOR,
                        (nx, ny, int(nw+1), int(nw+1))
                    )
                    gfxdraw.filled_circle(
                        screen,
                        int(nx + (nw/2)),
                        int(ny + (nw/2)),
                        int((nw * 0.8) / 2),
                        STUMP_COLOR
                    )

    def render_player(self, screen, camera):
        nx,ny,nw = self._coords_to_screen(screen, self.player.x, self.player.y, camera)
        pygame.draw.rect(
            screen,
            PLAYER_COLOR,
            (
                nx + (nw * PLAYER_SIZE), 
                ny + (nw * PLAYER_SIZE), 
                int((nw*(1-(PLAYER_SIZE*2)))+1), 
                int((nw*(1-(PLAYER_SIZE*2)))+1)
            )
        )

    def render_entities(self, screen, camera, bx, by):
        ent = self.em.in_bounds(bx, by)
        if self.transition is not None:
            ent = itertools.chain(ent, self.transition.entities())

        for e in ent:
            if not e.active:
                continue

            if e.x < bx[0] or e.x > bx[1] or e.y < by[0] or e.y > by[1]:
                continue

            nx,ny,nw = self._coords_to_screen(screen, e.x, e.y, camera)

            if type(e) is Log:
                if not e.is_raft:
                    if e.orientation is LogOrientation.STANDING:
                        gfxdraw.filled_circle(
                            screen,
                            int(nx + (nw/2)),
                            int(ny + (nw/2)),
                            int((nw * (1-(2*TREE_SIZE))) / 2),
                            TREE_COLOR
                        )
                        pass
                    elif e.orientation is LogOrientation.HORIZONTAL:
                        pygame.draw.rect(
                            screen,
                            TREE_COLOR,
                            (nx+(nw*0.1), ny+(nw*TREE_SIZE), int((nw*0.8)+1), int((nw*(1 - (2*TREE_SIZE)))+1))
                        )
                    elif e.orientation is LogOrientation.VERTICAL:
                        pygame.draw.rect(
                            screen,
                            TREE_COLOR,
                            (nx+(nw*TREE_SIZE), ny+(nw*0.1), int((nw*(1-(2*TREE_SIZE)))+1), int((nw*0.8)+1))
                        )
                else:
                    # render raft
                    pygame.draw.rect(
                        screen,
                        TREE_COLOR,
                        (nx+(nw*0.1), ny+(nw*0.15), int((nw*0.8)+1), int((nw*0.3)+1))
                    )
                    pygame.draw.rect(
                        screen,
                        TREE_COLOR,
                        (nx+(nw*0.1), ny+(nw*0.55), int((nw*0.8)+1), int((nw*0.3)+1))
                    )

    def render(self, screen, camera):
        width, height = screen.get_size()
        screen.fill(WATER_COLOR)

        dx = (float(width) / 2) / (camera.zoom * GRID_SIZE)
        bx = (
            _bound(int(camera.x - dx), 0, self.width),
            _bound(int(camera.x + dx + 1), 0, self.width)
        )

        dy = (float(height) / 2) / (camera.zoom * GRID_SIZE)
        by = (
            _bound(int(camera.y - dy), 0, self.height),
            _bound(int(camera.y + dy + 1), 0, self.height)
        )

        self.render_base(screen, camera, bx, by)
        self.render_entities(screen, camera, bx, by)
        self.render_player(screen, camera)

    def update(self, dt):
        if self.transition is not None:
            self.transition.update(dt)
            if self.transition.is_complete():
                self.history.append(self.transition)
                self.transition = None

    def undo(self):
        if len(self.history) > 0:
            t = self.history.pop(-1)
            t.backward()

    def entities_at(self, tx, ty):
        return self.em.at(tx,ty)

    def entity(self, tx, ty):
        ent = self.entities_at(tx, ty)
        if len(ent) > 1:
            assert False, 'Multiple entities'
        obj = ent[0] if len(ent) == 1 else None
        return obj

    def is_idle(self):
        return self.transition is None

    def roll_log(self, log, dx, dy):
        x = log.lx
        y = log.ly

        n = 0
        while True:
            ax = x + (dx * (n+1))
            ay = y + (dy * (n+1))

            ent = self.entity(ax, ay)

            if self.dat[ay][ax] == Tiles.WATER:
                if ent is None:
                    # Roll into water.
                    self.transition = Transition([TreeRollAnimation(
                        log, ax, ay, n+1
                    )])
                    return
                elif ent.is_raft:
                    pass
                else:
                    # Roll onto log.
                    if log.orientation == ent.orientation:
                        # Make a raft
                        self.transition = Transition([
                            TreeRollAnimation(log, ax-dx, ay-dy, n),
                            MakeRaftAnimation(log, ent, ax, ay)
                        ])
                        return
                    else:
                        # Keep rolling.
                        pass
            elif self.dat[ay][ax] in [Tiles.STUMP, Tiles.LAND_ROCK]:
                # Hit blocker.
                self.transition = Transition([TreeRollAnimation(
                    log, ax-dx, ay-dy, n
                )])
                return
            elif self.dat[ay][ax] == Tiles.LAND:
                if ent is not None:
                    # Hit blocker
                    self.transition = Transition([TreeRollAnimation(
                        log, ax-dx, ay-dy, n
                    )])
                    return
                else:
                    pass
            else:
                assert False

            n += 1

    def raw_push_log(self, log, tx, ty, ent):
        if ent is None:
            if self.dat[ty][tx] == Tiles.WATER:
                self.transition = Transition([TreeIntoWaterAnimation(log, tx, ty)])
            elif self.dat[ty][tx] == Tiles.LAND:
                self.transition = Transition([TreeFallAnimation(log, tx, ty)])
            elif self.dat[ty][tx] == Tiles.STUMP:
                self.transition = Transition([TreeFallAnimation(log, tx, ty)])
            else:
                pass # Log blocked
        elif ent.is_raft:
            pass
        else:
            if self.dat[ty][tx] == Tiles.WATER:
                self.transition = Transition([MakeRaftAnimation(log, ent, tx, ty)])
            elif self.dat[ty][tx] == Tiles.LAND:
                pass
            elif self.dat[ty][tx] == Tiles.STUMP:
                pass
            else:
                pass

    def push_log(self, log, dx, dy):
        cx = log.lx
        cy = log.ly
        tx = cx + dx
        ty = cy + dy

        ent = self.entity(tx, ty)

        # Target in map.
        if ty < 0 or ty >= self.height or tx < 0 or tx >= self.width:
            return

        if log.orientation == LogOrientation.STANDING:
            self.raw_push_log(log, tx, ty, ent)
        elif log.orientation == LogOrientation.VERTICAL:
            if dx != 0:
                self.roll_log(log, dx, dy)
            else:
                self.raw_push_log(log, tx, ty, ent)
        elif log.orientation == LogOrientation.HORIZONTAL:
            if dy != 0:
                self.roll_log(log, dx, dy)
            else:
                self.raw_push_log(log, tx, ty, ent)
        else:
            assert False

    def compute_raft(self, player, raft, dx, dy):
        x = raft.lx
        y = raft.ly

        n = 0
        while True:
            ax = x + (dx * (n+1))
            ay = y + (dy * (n+1))

            ent = self.entity(ax, ay)

            if ent is None:
                if self.dat[ay][ax] != Tiles.WATER:
                    # Stop if hitting land or rock.
                    self.transition = Transition([RaftAnimation(
                        player, raft, ax-dx, ay-dy, n
                    )])
                    return
                else:
                    pass
            else:
                # Stop if hitting log or raft
                self.transition = Transition([RaftAnimation(
                    player, raft, ax-dx, ay-dy, n
                )])
                return

            n += 1

    def try_move(self, dx, dy):
        cx = self.player.lx
        cy = self.player.ly
        tx = cx + dx
        ty = cy + dy

        ent = self.entity(cx, cy)
        ent_t = self.entity(tx, ty)

        # Target in map.
        if ty < 0 or ty >= self.height or tx < 0 or tx >= self.width:
            return

        if self.dat[cy][cx] == Tiles.LAND:
            if ent is None:
                # None/Land
                if ent_t is None:
                    # No target entity
                    if self.dat[ty][tx] in [Tiles.LAND, Tiles.STUMP]:
                        self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                    else:
                        return
                elif ent_t.is_raft:
                    # Raft target
                    if self.dat[ty][tx] == Tiles.WATER:
                        self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                    else:
                        pass
                else:
                    if self.dat[ty][tx] in [Tiles.LAND, Tiles.STUMP]:
                        # Pushing a log.
                        self.push_log(ent_t, dx, dy)
                    elif self.dat[ty][tx] == Tiles.WATER:
                        # Onto water log.
                        if ent_t.orientation == LogOrientation.STANDING:
                            assert False
                        elif ent_t.orientation == LogOrientation.VERTICAL:
                            if dx != 0:
                                return
                            else:
                                self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                        elif ent_t.orientation == LogOrientation.HORIZONTAL:
                            if dy != 0:
                                return
                            else:
                                self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                        else:
                            assert False
                    else:
                        pass
            elif ent.is_raft:
                # Raft/Land
                pass
            else:
                # Log/Land
                # Log on land, move in any direction if unobstructed.
                if self.dat[ty][tx] == Tiles.LAND_ROCK:
                    return # obstructed by rock
                elif self.dat[ty][tx] == Tiles.LAND:
                    if ent_t is None:
                        self.transition = Transition([
                            PlayerMoveAnimation(self.player, tx, ty)
                        ])
                    else:
                        pass
                elif self.dat[ty][tx] == Tiles.STUMP:
                    if ent_t is None:
                        self.transition = Transition([
                            PlayerMoveAnimation(self.player, tx, ty)
                        ])
                    else:
                        pass
                elif self.dat[ty][tx] == Tiles.WATER:
                    pass
                else:
                    assert False

        elif self.dat[cy][cx] == Tiles.STUMP:
            # Move from stump.
            if ent is None:
                if ent_t is None:
                    # No target entity
                    if self.dat[ty][tx] in [Tiles.LAND, Tiles.STUMP]:
                        self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                    else:
                        return
                elif ent_t.is_raft:
                    # Raft target
                    if self.dat[ty][tx] == Tiles.WATER:
                        self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                    else:
                        pass
                else:
                    # Moving onto or pushing a log.
                    if ent_t.orientation == LogOrientation.STANDING:
                        self.push_log(ent_t, dx, dy)
                    elif ent_t.orientation == LogOrientation.VERTICAL:
                        if dx != 0:
                            return
                        else:
                            self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                    elif ent_t.orientation == LogOrientation.HORIZONTAL:
                        if dy != 0:
                            return
                        else:
                            self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                    else:
                        assert False
            elif ent.is_raft:
                pass
            else:
                assert False
        
        elif self.dat[cy][cx] == Tiles.WATER:
            # Move from water.
            if ent is None:
                assert False # Drowning!
            elif ent.is_raft:
                if ent_t is None:
                    if self.dat[ty][tx] in [Tiles.LAND, Tiles.STUMP]:
                        self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                    elif self.dat[ty][tx] == Tiles.LAND_ROCK:
                        # Move raft.
                        self.compute_raft(self.player, ent, -dx, -dy)
                    else:
                        pass
                elif ent_t.is_raft:
                    pass
                else:
                    pass
            else:
                if self.dat[ty][tx] in [Tiles.LAND, Tiles.STUMP]:
                    if ent_t is None:
                        if ent.orientation == LogOrientation.STANDING:
                            assert False
                        elif ent.orientation == LogOrientation.VERTICAL:
                            if dy != 0:
                                self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                            else:
                                return
                        elif ent.orientation == LogOrientation.HORIZONTAL:
                            if dx != 0:
                                self.transition = Transition([PlayerMoveAnimation(self.player, tx, ty)])
                            else:
                                return
                        else:
                            assert False
                    elif ent_t.is_raft:
                        pass
                    else:
                        pass
                elif self.dat[ty][tx] == Tiles.WATER:
                    pass
                elif self.dat[ty][tx] == Tiles.STUMP:
                    pass
                elif self.dat[ty][tx] == Tiles.LAND_ROCK:
                    return # Blocked
                else:
                    assert False

        else:
            assert False
