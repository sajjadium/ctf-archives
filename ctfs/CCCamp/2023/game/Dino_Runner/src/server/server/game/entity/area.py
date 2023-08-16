import math
import operator
import random
import uuid
from dataclasses import dataclass
from functools import reduce
from typing import Any

import server
from server.game.entity.object import Object as EntityObject
from server.game.entity.pickupable import Pickupable
from server.game.map.properties import CustomInteraction, Interaction, InteractionOn
from shared.gen.messages.v1 import Interact, InteractStatus, InteractType, Item
from shared.gen.messages.v1 import Object as ObjectProto
from shared.gen.messages.v1 import Objects, ObjectType, Polygon, ServerMessage

ORES = [
    (
        Item(
            name="Common ore",
            description="",
            quantity=1,
            icon=2440,
        ),
        3,
    ),
    (
        Item(
            name="Medium rare ore",
            description="",
            quantity=1,
            icon=2441,
        ),
        181,
    ),
    (
        Item(
            name="Rare ore",
            description="",
            quantity=1,
            icon=2442,
        ),
        691,
    ),
    (
        Item(
            name="Epic ore",
            description="",
            quantity=1,
            icon=2443,
        ),
        4943,
    ),
    (
        Item(
            name="Legendary ore",
            description="",
            quantity=1,
            icon=2444,
        ),
        31337,
    ),
]


class Rng:
    state: int

    def __init__(self, seed: int) -> None:
        self.state = seed
        self.p = [x[1] for x in ORES]
        self.m = reduce(operator.mul, self.p)

    def next(self, offset: int) -> Item | None:
        offset %= self.m
        if offset == 0:
            return None
        r = math.gcd(self.m, offset)
        self.state += 1
        print("on offset", offset, r, self.state)
        if r == 1 or r not in self.p:
            return None
        # TODO with which propability? should we get the ore at the coord?
        # if ((self.state * offset)) % self.m == 0:
        return ORES[self.p.index(r)][0]
        # return -1


@dataclass(kw_only=True)
class AreaObject(EntityObject):
    area: Polygon
    user_uuid: str | None

    def __init__(
        self,
        interaction: Interaction,
        area: Polygon,
        interaction_on: InteractionOn,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.area = area
        self.user_uuid = None
        self.interaction = interaction
        self.interaction_on = interaction_on
        self.type = ObjectType.OBJECT_TYPE_AREA
        self.dig = None
        self.actice = False

    def to_proto(self) -> ObjectProto:
        o = super().to_proto()

        o.area = self.area

        return o

    async def interact(self, user_id: str, interact: Interact) -> Interact | None:
        return None

    def in_range(self, user_id: str) -> Interact | None:
        self.actice = True

        return Interact(
            str(uuid.uuid4()),
            status=InteractStatus.INTERACT_STATUS_START,
            type=InteractType.INTERACT_TYPE_CUT_OUT,
        )

    def out_of_range(self, user_id: str) -> Interact | None:
        self.actice = False

        return Interact(
            str(uuid.uuid4()),
            status=InteractStatus.INTERACT_STATUS_STOP,
            type=InteractType.INTERACT_TYPE_CUT_OUT,
        )


class DigProgress:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.progress = 0.0
        pass


class DigArea(AreaObject):
    def __init__(
        self,
        interaction: Interaction,
        area: Polygon,
        interaction_on: InteractionOn,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(interaction, area, interaction_on, *args, **kwargs)
        self.dig = None
        self.rng = Rng(random.randint(1, 31337))

    async def interact(self, user_id: str, interact: Interact) -> Interact | None:
        assert self.interaction.custom_interaction == CustomInteraction.DIG
        user = server.game_state.get_user(user_id)
        assert user
        if next((x for x in user.inventory if x.name == "Shovel"), None) is None:
            return None
        match interact.status:
            case InteractStatus.INTERACT_STATUS_START:
                self.dig = DigProgress(user.coords.x, user.coords.y)
                return Interact(
                    interact.uuid,
                    "",
                    status=InteractStatus.INTERACT_STATUS_START,
                    progress=self.dig.progress,
                    type=InteractType.INTERACT_TYPE_DIG,
                )

            case InteractStatus.INTERACT_STATUS_UPDATE:
                assert self.dig
                if self.dig.x != user.coords.x or self.dig.y != user.coords.y:
                    return None
                self.dig.progress += 1 / 10
                if self.dig.progress >= 0.999:
                    val = self.rng.next(int(self.dig.x + self.dig.y * 1337))
                    if val is not None:
                        ore = Pickupable(
                            x=self.dig.x,
                            y=self.dig.y + 20,
                            item=val,
                            name="ore",
                            direction=0,
                            for_everyone=False,
                            garbage_collect_on_pickup=True,
                        )
                        server.game_state.pickupable_manager.deepcopy_add(user_id, ore)
                        session = server.game_state.get_session(user_id)
                        assert session
                        server.game_state.user_sessions[user.uuid].known_objects |= set(
                            [ore.uuid]
                        )
                        response = ServerMessage(
                            objects=Objects(objects=[ore.to_proto()]),
                        )
                        await server.global_server.broadcast(
                            response, include=[session]
                        )

                    return Interact(
                        interact.uuid,
                        text=f"You found {val}",
                        status=InteractStatus.INTERACT_STATUS_STOP,
                        progress=self.dig.progress,
                        type=InteractType.INTERACT_TYPE_DIG,
                    )
                return Interact(
                    uuid=interact.uuid,
                    text="",
                    status=InteractStatus.INTERACT_STATUS_UPDATE,
                    progress=self.dig.progress,
                    type=InteractType.INTERACT_TYPE_DIG,
                )
            case _:
                pass
