from dataclasses import dataclass
from typing import Any

import server
from server.game.entity.object import Object
from shared.gen.messages.v1 import Item
from shared.gen.messages.v1 import Object as ObjectProto
from shared.gen.messages.v1 import Object as ProtoObject
from shared.gen.messages.v1 import Objects, ObjectType, ServerMessage, SessionType, User


@dataclass(kw_only=True)
class Pickupable(Object):
    user_uuid: str | None

    def __init__(
        self,
        item: Item,
        for_everyone: bool,
        garbage_collect_on_pickup: bool,
        *args: Any,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)

        self.pickupable = item
        self.type = ObjectType.OBJECT_TYPE_PICKUPABLE
        self.user_uuid = None
        self.pickedup = False
        self.for_everyone = for_everyone
        self.garbage_collect_on_pickup = garbage_collect_on_pickup

    def in_distance_to_player(self, user: User) -> bool:
        player_asset = server.game_state.map.player_asset

        dx = (user.coords.x + player_asset.width / 2) - ((self.x + 16 / 2))
        dy = (user.coords.y - player_asset.height / 2) - ((self.y - 16 / 2))
        distance_sq = dx**2 + dy**2

        return distance_sq < 14**2

    async def update(self, dt: float) -> None:
        if not self.pickedup:
            if self.user_uuid and self.user_uuid in server.game_state.users:
                user = server.game_state.users[self.user_uuid]

                if user.uuid not in server.game_state.user_sessions:
                    return

                session = server.game_state.user_sessions[user.uuid]

                if session.type == SessionType.SESSION_TYPE_FREE_CAM:
                    return

                if self.in_distance_to_player(user):
                    self.pickedup = True

                    await server.game_state.give_item(self.user_uuid, self.pickupable)
                    await server.global_server.broadcast(
                        ServerMessage(
                            objects=Objects(
                                objects=[
                                    ProtoObject(
                                        self.uuid,
                                        remove=True,
                                        type=ObjectType.OBJECT_TYPE_PICKUPABLE,
                                    )
                                ]
                            )
                        ),
                        include=[session.peer],
                    )

            elif self.for_everyone:
                for user_id in server.game_state.user_sessions.keys():
                    if user_id not in server.game_state.users:
                        continue

                    user = server.game_state.users[user_id]

                    session = server.game_state.user_sessions[user.uuid]
                    if session.type == SessionType.SESSION_TYPE_FREE_CAM:
                        continue

                    if self.in_distance_to_player(user):
                        self.pickedup = True

                        await server.game_state.give_item(user_id, self.pickupable)
                        await server.global_server.broadcast(
                            ServerMessage(
                                objects=Objects(
                                    objects=[
                                        ProtoObject(
                                            self.uuid,
                                            remove=True,
                                            type=ObjectType.OBJECT_TYPE_PICKUPABLE,
                                        )
                                    ]
                                )
                            ),
                            include=[session.peer],
                        )

                        break

        return await super().update(dt)

    def to_proto(self) -> ObjectProto:
        proto = super().to_proto()

        proto.pickupable = self.pickupable

        return proto
