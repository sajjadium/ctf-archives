from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

import client
from client.game.entities.entity import Direction
from shared.gen.messages.v1 import Interact, InteractStatus, InteractType, Polygon

if TYPE_CHECKING:
    from client.scenes.game import Game


@dataclass
class Area:
    uuid: str

    def __init__(self, uuid: str, area: Polygon, *args: int, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)
        self.area = area
        self.uuid = uuid
        self.in_interaction = False

    def on_interaction(self, interact: Interact):
        game = cast("Game", client.scene_manager.current_scene)
        player = game.player

        match interact.type:
            case InteractType.INTERACT_TYPE_DIG:
                match interact.status:
                    case InteractStatus.INTERACT_STATUS_START:
                        self.in_interaction = True
                        player.can_move = False
                        player.direction = Direction.UP
                        player.progress = interact.progress
                    case InteractStatus.INTERACT_STATUS_UPDATE:
                        player.progress = interact.progress
                        pass
                    case InteractStatus.INTERACT_STATUS_STOP:
                        self.in_interaction = False
                        player.can_move = True
                        player.progress = -1
                    case InteractStatus.INTERACT_STATUS_UNSPECIFIED:
                        assert False
            case _:
                pass

    def interact(self):
        if self.in_interaction:
            client.global_connection.interact(
                self.uuid,
                text="",
                status=InteractStatus.INTERACT_STATUS_UPDATE,
                handler=self.on_interaction,
            )
        else:
            client.global_connection.interact(
                self.uuid,
                text="",
                status=InteractStatus.INTERACT_STATUS_START,
                handler=self.on_interaction,
            )

    def stop_interaction(self) -> None:
        if self.in_interaction:
            client.global_connection.interact(
                self.uuid,
                text="",
                status=InteractStatus.INTERACT_STATUS_STOP,
                handler=self.on_interaction,
            )
