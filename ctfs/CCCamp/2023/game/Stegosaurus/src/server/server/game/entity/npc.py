import json
import logging
import math
import random
from copy import copy
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any, List, Tuple, cast

import server
from server.game.entity.dino_runner import Engine
from server.game.entity.object import Object
from server.game.map.properties import CustomInteraction
from server.game.secret import ITEMS
from server.models import ScoreboardEntry
from shared.gen.messages.v1 import (EntityAsset, EntityAssets, Interact,
                                    InteractStatus, InteractType, Item)
from shared.gen.messages.v1 import Object as ObjectProto
from shared.gen.messages.v1 import (ObjectType, Polygon, ShopInteract,
                                    ShopInteractType)

# This comes from the native python module, redacted here
# from license_checker import check_license  # type: ignore


shop_items: Any = None


def get_random_shop_item(exclude: Item | None = None) -> Item:
    global shop_items

    if shop_items is None:
        with open(Path(server.PATH, "./map/items.json")) as f:
            shop_items = json.load(f)["items"]

    possibilities = shop_items.copy()

    if exclude:
        possibilities = [p for p in possibilities if p["name"] != exclude.name]

    item = random.choice(possibilities)

    item_proto = Item().from_dict(item)
    item_proto.quantity = random.randint(1, 3)

    return item_proto


@dataclass
class NPCPath:
    path: Polygon
    current_path_step: int
    speed: float
    loop: bool

    def __init__(self, path: Polygon | None, speed: float, loop: bool = False):
        match path:
            case None:
                self.path = Polygon()
            case p:
                self.path = p

        self.current_path_step = 0
        self.speed = speed
        self.loop = loop

    def reset(self):
        self.current_path_step = 0

    def get_next_position(self, dt: float, x: float, y: float) -> Tuple[float, float]:
        if self.current_path_step > len(self.path.points) or len(self.path.points) == 0:
            return (x, y)

        next_point = self.path.points[self.current_path_step % len(self.path.points)]

        if x == next_point.x and y == next_point.y:
            self.current_path_step += 1

            if self.loop:
                self.current_path_step %= len(self.path.points)

            next_point = self.path.points[
                self.current_path_step % len(self.path.points)
            ]

        dx = next_point.x - x
        dy = next_point.y - y

        l = math.sqrt(dx**2 + dy**2)

        dx *= 1 / l
        dy *= 1 / l

        distance_x = dx * self.speed * dt
        distance_y = dy * self.speed * dt

        max_l = math.sqrt(distance_x**2 + distance_y**2)

        if max_l > l:
            distance_x = dx * l
            distance_y = dy * l

        next_x = x + distance_x
        next_y = y + distance_y

        x = next_x
        y = next_y

        return (x, y)


@dataclass
class Interaction:
    id: int
    _text: str

    path: NPCPath
    speed: float
    loop: bool
    current_path_step: int

    next_interaction: int

    custom_interaction: CustomInteraction
    custom_attribute: str

    def __init__(
        self,
        id: int,
        text: str,
        path: Polygon | None,
        speed: float,
        loop: bool,
        custom_interaction: CustomInteraction,
        custom_attribute: str,
        current_path_step: int = 0,
        next_interaction: int = -1,
    ) -> None:
        match path:
            case None:
                self.path = NPCPath(path=None, speed=speed, loop=loop)
            case p:
                self.path = NPCPath(path=p, speed=speed, loop=loop)

        self.id = id
        self._text = text
        self.speed = speed
        self.loop = loop
        self.custom_interaction = custom_interaction
        self.custom_attribute = custom_attribute

        self.current_path_step = current_path_step
        self.next_interaction = next_interaction

        if self.custom_interaction == CustomInteraction.TALKY:
            with open(Path(server.PATH, custom_attribute), "r") as f:
                self._text = f.read()

    @property
    async def text(self) -> str:
        match self.custom_interaction:
            case CustomInteraction.REQUIRE_ITEMS:
                # this is fine :mildpanic:
                req = eval(self.custom_attribute)

                return self._text.replace(
                    r"%items",
                    ",".join([f"{y}x {x}" for (x, y) in req.items()]),
                )

            case CustomInteraction.TALKY:
                if len(self._text) == 0:
                    with open(Path(server.PATH, self.custom_attribute), "r") as f:
                        self._text = f.read()

                    return ""

                split = self._text.split("\n", 1)
                passage = split[0]
                if len(passage) <= 200:
                    if len(split) > 1:
                        self._text = split[1]
                    else:
                        self._text = ""
                else:
                    passage = passage[:200].rsplit(" ", 1)[0]
                    self._text = self._text[len(passage) :]

                passage = passage.lstrip()

                return passage
            case CustomInteraction.SCOREBOARD:
                # scoreboard: list[ScoreboardEntry] = [
                #     e for e in server.game_state.scoreboard.values() if e.time
                # ]
                scoreboard: list[ScoreboardEntry] = [
                    e for e in await server.game_state.get_remote_scoreboard() if e.time
                ]
                scoreboard.sort(key=lambda e: e.time if e.time else timedelta.max)

                return "\n".join(
                    [
                        f"#{i} {user} {time} "
                        for i, (time, user) in enumerate(
                            (
                                e.time,
                                e.username,
                            )
                            for e in scoreboard
                        )
                        if user
                    ]
                )
            case _:
                return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    @property
    def interaction_type(self) -> InteractType:
        match self.custom_interaction:
            case CustomInteraction.SHOP:
                return InteractType.INTERACT_TYPE_SHOP
            case CustomInteraction.RUNNER:
                return InteractType.INTERACT_TYPE_RUNNER
            case CustomInteraction.LICENSE:
                return InteractType.INTERACT_TYPE_LICENSE
            case _:
                return InteractType.INTERACT_TYPE_TEXT

    @property
    def shop(self) -> list[ShopInteract]:
        shop: list[ShopInteract] = []

        match self.custom_interaction:
            case CustomInteraction.SHOP:
                pass
            case _:
                return shop

        shop.append(
            ShopInteract(
                item=copy(ITEMS["flag_merchant"]),
                cost=1000000,
                type=ShopInteractType.SHOP_INTERACT_TYPE_SELL,
            )
        )

        for _ in range(random.randrange(1, 11)):
            match random.randrange(3):
                case 0:
                    shop.append(
                        ShopInteract(
                            item=get_random_shop_item(),
                            type=ShopInteractType.SHOP_INTERACT_TYPE_BUY,
                            cost=random.randrange(750, 1000),
                        )
                    )
                case 1:
                    shop.append(
                        ShopInteract(
                            item=get_random_shop_item(),
                            type=ShopInteractType.SHOP_INTERACT_TYPE_SELL,
                            cost=random.randrange(750, 1000),
                        )
                    )
                case 2:
                    item = get_random_shop_item()

                    shop.append(
                        ShopInteract(
                            item=item,
                            type=ShopInteractType.SHOP_INTERACT_TYPE_TRADE,
                            trade_in=get_random_shop_item(item),
                        )
                    )
                case _:
                    pass

        return shop

    def reset(self) -> None:
        self.current_path_step = 0

    def move(self, dt: float, x: float, y: float) -> Tuple[float, float]:
        if self.path:
            x, y = self.path.get_next_position(dt, x, y)

        return (x, y)


@dataclass(kw_only=True)
class NPC(Object):
    interactable: bool
    interact_distance: float
    interaction_step: int
    interactions: List[Interaction]
    entity_asset: EntityAsset

    user_uuid: str | None

    def __init__(
        self,
        interactable: bool,
        interact_distance: float,
        interactions: List[Interaction],
        entity_assets: EntityAssets,
        user_uuid: str | None = None,
        interaction_step: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.interactable = interactable
        self.interact_distance = interact_distance
        self.interactions = interactions

        self.user_uuid = user_uuid

        self.interaction_step = interaction_step
        self.entity_assets = entity_assets
        self.runner_seed = None

        super().__init__(*args, **kwargs)
        self.type = ObjectType.OBJECT_TYPE_NPC

    async def update(self, dt: float) -> None:
        await super().update(dt=dt)

        current_interaction = (
            self.interactions[self.interaction_step]
            if self.interaction_step < len(self.interactions)
            else None
        )
        if current_interaction is not None:
            next_x, next_y = current_interaction.move(dt, self.x, self.y)

            moved = True if self.x != next_x or self.y != next_y else False

            self.x = next_x
            self.y = next_y

            if self.user_uuid is not None:
                await server.global_server.move_object(
                    self.uuid, self.x, self.y, include_user_ids=[self.user_uuid]
                )
            elif moved:
                await server.global_server.move_object(self.uuid, self.x, self.y)

    def _step_interact(self) -> None:
        current_interaction = self.interactions[self.interaction_step]

        if current_interaction.next_interaction == -1:
            next_interaction_id = (self.interaction_step + 1) % len(self.interactions)
        else:
            next_interaction_id = current_interaction.next_interaction

        self.interaction_step = next_interaction_id

        interaction = self.interactions[next_interaction_id]
        interaction.reset()

    # This is actually in the native build module. Just a placeholder here
    def check_license(
        self, _num
    ):
        return 1

    async def interact(self, user_id: str, interact: Interact) -> Interaction:
        current_interaction = self.interactions[self.interaction_step]

        should_skip = False

        match current_interaction.interaction_type:
            case InteractType.INTERACT_TYPE_LICENSE:
                try:
                    val = int(interact.text, 16) & 0xFFFFFFFFFFFFFFFF
                    ret = cast(int, check_license(val))
                    match ret:
                        case 1:
                            should_skip = True
                            self.interaction_step += 2
                            self.interaction = self.interactions[self.interaction_step]
                            self.interaction.reset()
                            self.interaction.text = (
                                await self.interaction.text
                            ).replace(r"%item", r"LOCALO")
                            success = await server.game_state.give_item(
                                user_id, ITEMS["localo"], True
                            )
                            if success:
                                await server.global_server.update_self(user_id)
                        case 2:
                            should_skip = True
                            self.interaction_step += 2
                            self.interaction = self.interactions[self.interaction_step]
                            self.interaction.reset()
                            self.interaction.text = (
                                await self.interaction.text
                            ).replace(r"%item", r"FLAG")
                            success = await server.game_state.give_item(
                                user_id, ITEMS["flag_license"], True
                            )
                            if success:
                                await server.global_server.update_self(user_id)
                        case _:
                            pass
                except:
                    pass
                pass
            case InteractType.INTERACT_TYPE_SHOP:
                if len(interact.shop) > 0:
                    flag = ITEMS["flag_merchant"]

                    i = interact.shop[0]

                    for item in shop_items:
                        if item["name"] == i.item.name:
                            i.item.description = item["description"]
                            break

                    if i.item.name == flag.name:
                        i.item.description = flag.description

                    if i.trade_in:
                        for item in shop_items:
                            if item["name"] == i.trade_in.name:
                                i.trade_in.description = item["description"]
                                break

                        if i.trade_in.name == flag.name:
                            i.trade_in.description = flag.description

                    success = server.game_state.shop(user_id, i)
                    if success:
                        await server.global_server.update_self(user_id)
            case _:
                pass

        if not should_skip:
            self._step_interact()

        interaction = self.interactions[self.interaction_step]
        match interaction.custom_interaction:
            case CustomInteraction.REQUIRE_ITEMS:
                reqs = eval(interaction.custom_attribute)
                user = server.game_state.get_user(user_id)
                assert user
                for i, q in reqs.items():
                    item = next((x for x in user.inventory if x.name == i), None)
                    if item is None:
                        break
                    if item.quantity < q:
                        break
                else:
                    for i, q in reqs.items():
                        item = next((x for x in user.inventory if x.name == i))
                        item.quantity -= q
                        if item.quantity == 0:
                            user.inventory.remove(item)
                    await server.global_server.update_self(user_id)

                    self.interaction_step += 2

                    self.interaction = self.interactions[self.interaction_step]
                    self.interaction.reset()

            case CustomInteraction.RUNNER:
                if (
                    interact.status == InteractStatus.INTERACT_STATUS_STOP
                    and self.runner_seed is not None
                ):
                    runner = interact.runner
                    sim = Engine()
                    sim.seed = self.runner_seed
                    result, _time, score = sim.run(runner)
                    if result and score > 1337:
                        success = await server.game_state.give_item(
                            user_id, ITEMS["flag_runner"], True
                        )
                        if success:
                            await server.global_server.update_self(user_id)
                    self.runner_seed = None
                if interact.status == InteractStatus.INTERACT_STATUS_UPDATE:
                    if self.runner_seed == None:
                        self.runner_seed = random.random() * 31337

            case CustomInteraction.RACE_START:
                server.game_state.start_timer(user_id=user_id)
                self._step_interact()
            case CustomInteraction.RACE_STOP:
                entry = await server.game_state.stop_timer(user_id=user_id)
                race_to_reach = timedelta(minutes=1, seconds=20, milliseconds=750)

                if entry is None:
                    self._step_interact()
                elif entry.time < race_to_reach:
                    interaction._text = f"Your found me, in {entry.time}. Good job, I gave you a flag to keep."
                    success = await server.game_state.give_item(
                        user_id, ITEMS["flag_race_to_top"], True
                    )
                    if success:
                        await server.global_server.update_self(user_id)
                else:
                    interaction._text = f"You found me, but it took {entry.time}, try again and get faster than {race_to_reach}."
            case CustomInteraction.GIVE_ITEM:
                if interaction.custom_attribute not in ITEMS:
                    logging.warn(f"Unknown ITEM {interaction.custom_attribute}")
                else:
                    success = await server.game_state.give_item(
                        user_id, ITEMS[interaction.custom_attribute], True
                    )
                    if success:
                        await server.global_server.update_self(user_id)
            case _:
                pass

        interaction = self.interactions[self.interaction_step]
        return interaction

    def to_proto(self) -> ObjectProto:
        return super().to_proto()
