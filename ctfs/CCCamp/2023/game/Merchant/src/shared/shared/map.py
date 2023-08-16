from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

from shared.gen.messages.v1 import Polygon


@dataclass
class Tile:
    chunk_atlas_offset: int
    collision: List[Polygon]


class Map(ABC):
    @abstractmethod
    def get_tiles(
        self, x: float, y: float, user_id: str
    ) -> Tuple[List[Tile], float, float] | None:
        pass
