from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from server.game.state import Game
from server.server_runner import Server

game_state: Game
global_server: Server
executor: ProcessPoolExecutor

PATH = Path(__file__).parent
