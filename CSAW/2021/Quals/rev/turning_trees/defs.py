
from enum import Enum

class LogOrientation(Enum):
    TREE = 0
    STANDING = 1
    VERTICAL = 2
    HORIZONTAL = 3

    TRANSITION_UP = 4
    TRANSITION_DOWN = 5
    TRANSITION_LEFT = 6
    TRANSITION_RIGHT = 7


class Tiles(object):
    WATER = 1
    LAND = 2
    STUMP = 3
    LAND_ROCK = 4
