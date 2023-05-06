
import itertools
from typing import List
from enum import Enum

from .constants import ANIMATION_SPEED
from .defs import LogOrientation


def ease_in_out(t,a,b):
    fac = 4 * t**3 if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2
    return (float(a) * (1 - fac)) + (float(b) * fac)


def linear(t,a,b):
    fac = t
    return (float(a) * (1 - fac)) + (float(b) * fac)


class Animation(object):
    SPEED = ANIMATION_SPEED

    def _curr(self, et, start, stop):
        off = (et - (start * Animation.SPEED)) / (stop * Animation.SPEED)
        return max(min(off, 1), 0)


class PlayerMoveAnimation(Animation):
    tx: int
    tx: int
    ix: int
    ix: int

    def __init__(self, player, tx, ty):
        self.player = player
        self.tx = tx
        self.ty = ty
        self.ix = player.lx
        self.iy = player.ly

    def update(self, et):
        t = self._curr(et, 0, 1)
        self.player.x = ease_in_out(t, self.ix, self.tx)
        self.player.y = ease_in_out(t, self.iy, self.ty)
        return t >= 1

    def forward(self):
        self.player.lx = self.tx
        self.player.ly = self.ty
        self.player.x = float(self.tx)
        self.player.y = float(self.ty)

    def backward(self):
        self.player.lx = self.ix
        self.player.ly = self.iy
        self.player.x = float(self.ix)
        self.player.y = float(self.iy)

    def entities(self):
        return []

class TreeFallAnimation(Animation):
    log: 'Log'

    # Target.
    tx: int
    tx: int
    to: LogOrientation
    mo: LogOrientation # middle orientation

    # Initial.
    ix: int
    ix: int
    io: LogOrientation

    def __init__(self, log, tx, ty):
        self.log = log
        self.tx = tx
        self.ty = ty
        self.ix = log.lx
        self.iy = log.ly
        self.io = log.orientation

        to = None
        mo = None
        if log.orientation == LogOrientation.STANDING:
            if tx > self.ix:
                to = LogOrientation.HORIZONTAL
                mo = LogOrientation.TRANSITION_RIGHT
            elif tx < self.ix:
                to = LogOrientation.HORIZONTAL
                mo = LogOrientation.TRANSITION_LEFT
            elif ty < self.iy:
                to = LogOrientation.VERTICAL
                mo = LogOrientation.TRANSITION_UP
            elif ty > self.iy:
                to = LogOrientation.VERTICAL
                mo = LogOrientation.TRANSITION_DOWN
            else:
                assert False
        elif log.orientation == LogOrientation.HORIZONTAL:
            if tx > self.ix:
                to = LogOrientation.STANDING
                mo = LogOrientation.TRANSITION_LEFT
            elif tx < self.ix:
                to = LogOrientation.STANDING
                mo = LogOrientation.TRANSITION_RIGHT
            else:
                assert False
        elif log.orientation == LogOrientation.VERTICAL:
            if ty > self.iy:
                to = LogOrientation.STANDING
                mo = LogOrientation.TRANSITION_UP
            elif ty < self.iy:
                to = LogOrientation.STANDING
                mo = LogOrientation.TRANSITION_DOWN
            else:
                assert False
        else:
            assert False
        
        self.to = to
        self.mo = mo
        log.orientation = to
        log.fall_p = 0


    def update(self, et):
        t = self._curr(et, 0, 1)
        self.log.x = ease_in_out(t, self.ix, self.tx)
        self.log.y = ease_in_out(t, self.iy, self.ty)
        return t >= 1

    def forward(self):
        self.log.lx = self.tx
        self.log.ly = self.ty
        self.log.x = float(self.tx)
        self.log.y = float(self.ty)
        self.log.orientation = self.to
        self.log.update(self.ix, self.iy, self.tx, self.ty)

    def backward(self):
        self.log.lx = self.ix
        self.log.ly = self.iy
        self.log.x = float(self.ix)
        self.log.y = float(self.iy)
        self.log.orientation = self.io
        self.log.update(self.tx, self.ty, self.ix, self.iy)

    def entities(self):
        return [self.log]


class TreeIntoWaterAnimation(Animation):
    log: 'Log'

    # Target.
    tx: int
    tx: int
    to: LogOrientation
    mo: LogOrientation # middle orientation

    # Initial.
    ix: int
    ix: int
    io: LogOrientation

    def __init__(self, log, tx, ty):
        self.log = log
        self.tx = tx
        self.ty = ty
        self.ix = log.lx
        self.iy = log.ly
        self.io = log.orientation

        to = None
        mo = None
        if log.orientation == LogOrientation.STANDING:
            if tx > self.ix:
                to = LogOrientation.HORIZONTAL
                mo = LogOrientation.TRANSITION_RIGHT
            elif tx < self.ix:
                to = LogOrientation.HORIZONTAL
                mo = LogOrientation.TRANSITION_LEFT
            elif ty < self.iy:
                to = LogOrientation.VERTICAL
                mo = LogOrientation.TRANSITION_UP
            elif ty > self.iy:
                to = LogOrientation.VERTICAL
                mo = LogOrientation.TRANSITION_DOWN
            else:
                assert False
        elif log.orientation == LogOrientation.HORIZONTAL:
            if tx > self.ix:
                to = LogOrientation.HORIZONTAL
                mo = LogOrientation.HORIZONTAL
            elif tx < self.ix:
                to = LogOrientation.HORIZONTAL
                mo = LogOrientation.HORIZONTAL
            else:
                assert False
        elif log.orientation == LogOrientation.VERTICAL:
            if ty > self.iy:
                to = LogOrientation.VERTICAL
                mo = LogOrientation.VERTICAL
            elif ty < self.iy:
                to = LogOrientation.VERTICAL
                mo = LogOrientation.VERTICAL
            else:
                assert False
        else:
            assert False
        
        self.to = to
        self.mo = mo
        log.orientation = to
        log.fall_p = 0

    def update(self, et):
        t = self._curr(et, 0, 1)
        self.log.x = ease_in_out(t, self.ix, self.tx)
        self.log.y = ease_in_out(t, self.iy, self.ty)
        return t >= 1

    def forward(self):
        self.log.lx = self.tx
        self.log.ly = self.ty
        self.log.x = float(self.tx)
        self.log.y = float(self.ty)
        self.log.orientation = self.to
        self.log.update(self.ix, self.iy, self.tx, self.ty)

    def backward(self):
        self.log.lx = self.ix
        self.log.ly = self.iy
        self.log.x = float(self.ix)
        self.log.y = float(self.iy)
        self.log.orientation = self.io
        self.log.update(self.tx, self.ty, self.ix, self.iy)

    def entities(self):
        return [self.log]


class TreeRollAnimation(Animation):
    def __init__(self, log, tx, ty, n):
        self.log = log
        self.tx = tx
        self.ty = ty
        self.n = n

        self.ix = log.lx
        self.iy = log.ly

    def update(self, et):
        if self.n == 0:
            return True
        t = self._curr(et, 0, self.n / 2.0)
        self.log.x = linear(t, self.ix, self.tx)
        self.log.y = linear(t, self.iy, self.ty)
        return t >= 1

    def forward(self):
        self.log.lx = self.tx
        self.log.ly = self.ty
        self.log.x = float(self.tx)
        self.log.y = float(self.ty)
        self.log.update(self.ix, self.iy, self.tx, self.ty)

    def backward(self):
        self.log.lx = self.ix
        self.log.ly = self.iy
        self.log.x = float(self.ix)
        self.log.y = float(self.iy)
        self.log.update(self.tx, self.ty, self.ix, self.iy)

    def entities(self):
        return [self.log]


class MakeRaftAnimation(Animation):
    def __init__(self, log1, log2, tx, ty):
        # log1 is moving onto log2
        self.log1 = log1
        self.log2 = log2
        self.tx = tx
        self.ty = ty

        self.ix = log1.lx
        self.iy = log1.ly

    def update(self, et):
        t = self._curr(et, 0, 1)
        self.log1.x = ease_in_out(t, self.ix, self.tx)
        self.log1.y = ease_in_out(t, self.iy, self.ty)
        return t >= 1

    def forward(self):
        self.log1.lx = self.tx
        self.log1.ly = self.ty
        self.log1.x = float(self.tx)
        self.log1.y = float(self.ty)

        self.log1.is_raft = True
        self.log1.active = True
        self.log1.raft_partner = self.log2

        self.log2.is_raft = True
        self.log2.active = False
        self.log2.raft_partner = self.log1

        self.log1.update(self.ix, self.iy, self.tx, self.ty)

    def backward(self):
        self.log1.lx = self.ix
        self.log1.ly = self.iy
        self.log1.x = float(self.ix)
        self.log1.y = float(self.iy)

        self.log1.is_raft = False
        self.log1.raft_partner = None

        self.log2.is_raft = False
        self.log2.active = True
        self.log2.raft_partner = None

        self.log1.update(self.tx, self.ty, self.ix, self.iy)

    def entities(self):
        return [self.log1, self.log2]


class RaftAnimation(Animation):
    def __init__(self, player, raft, tx, ty, n):
        self.player = player
        self.raft = raft
        self.tx = tx
        self.ty = ty
        self.n = n
        
        self.ix = raft.lx
        self.iy = raft.ly

    def update(self, et):
        if self.n == 0:
            return True
        t = self._curr(et, 0, self.n)
        x = linear(t, self.ix, self.tx)
        y = linear(t, self.iy, self.ty)
        self.raft.x = x
        self.raft.y = y
        self.player.x = x
        self.player.y = y
        return t >= 1

    def forward(self):
        self.raft.lx = self.tx
        self.raft.ly = self.ty
        self.raft.x = float(self.tx)
        self.raft.y = float(self.ty)

        self.raft.raft_partner.lx = self.tx
        self.raft.raft_partner.ly = self.ty
        self.raft.raft_partner.x = float(self.tx)
        self.raft.raft_partner.y = float(self.ty)

        self.player.lx = self.tx
        self.player.ly = self.ty
        self.player.x = float(self.tx)
        self.player.y = float(self.ty)

        self.raft.update(self.ix, self.iy, self.tx, self.ty)
        self.raft.raft_partner.update(self.ix, self.iy, self.tx, self.ty)

    def backward(self):
        self.raft.lx = self.ix
        self.raft.ly = self.iy
        self.raft.x = float(self.ix)
        self.raft.y = float(self.iy)

        self.raft.raft_partner.lx = self.ix
        self.raft.raft_partner.ly = self.iy
        self.raft.raft_partner.x = float(self.ix)
        self.raft.raft_partner.y = float(self.iy)

        self.player.lx = self.ix
        self.player.ly = self.iy
        self.player.x = float(self.ix)
        self.player.y = float(self.iy)

        self.raft.update(self.tx, self.ty, self.ix, self.iy)
        self.raft.raft_partner.update(self.tx, self.ty, self.ix, self.iy)

    def entities(self):
        return [self.raft, self.raft.raft_partner]


class Transition(object):
    animations: List[Animation]
    complete: List[bool]
    
    def __init__(self, animations):
        self.animations = animations
        self.idx = 0
        self.et = 0

    def update(self, dt):
        self.et += dt

        if self.idx >= len(self.animations):
            return
        
        a = self.animations[self.idx]
        if a.update(self.et):
            self.idx += 1
            a.forward()

    def is_complete(self):
        return self.idx >= len(self.animations)

    def backward(self):
        for a in self.animations[::-1]:
            a.backward()

    def entities(self):
        return itertools.chain(*[a.entities() for a in self.animations])
