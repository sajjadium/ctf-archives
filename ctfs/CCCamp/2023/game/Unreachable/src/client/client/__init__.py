MOTION_SELECT_ALL = 0xFF
MOTION_DELETE_REST = 0xFE

from pathlib import Path

import pyglet
from pyglet.window import key

from client.game.state import GameState
from client.networking.network import Connection
from client.scenes.scenemanager import SceneManager

if hasattr(pyglet.window, "xlib"):
    pyglet.window.xlib._motion_map[(key.A, True)] = MOTION_SELECT_ALL  # type: ignore
    pyglet.window.xlib._motion_map[(key.DELETE, True)] = MOTION_DELETE_REST  # type: ignore
if hasattr(pyglet.window, "win32"):
    pyglet.window.win32._motion_map[(key.A, True)] = MOTION_SELECT_ALL  # type: ignore
    pyglet.window.win32._motion_map[(key.DELETE, True)] = MOTION_DELETE_REST  # type: ignore


MAP_SHADER = None
TILE_BOX_SHADER = None
global_connection: Connection
scene_manager: SceneManager
game_state: GameState


PATH = Path(__file__).parent
