from datetime import datetime, timedelta
from itertools import chain
from typing import Callable, Dict, cast

from pyglet.event import EVENT_HANDLED
from pyglet.graphics import Batch
from pyglet.gui import Frame
from pyglet.window import Window
from pyglet.window.key import ESCAPE, SPACE

import client
from client.game.area import Area
from client.game.camera import CenteredCamera
from client.game.entities.enemy import Enemy
from client.game.entities.entity import ServerManagedEntity
from client.game.entities.npc import NPC
from client.game.entities.other_player import OtherPlayer
from client.game.entities.player import Player
from client.game.map import ClientMap
from client.game.pickupable import Pickupable
from client.game.sound_manager import SoundManager
from client.scenes.dialog import DialogScene
from client.scenes.dino_runner import DinoRunner
from client.scenes.hud import Hud
from client.scenes.input import InputScene
from client.scenes.inventory import Inventory
from client.scenes.scenemanager import Scene
from client.scenes.shop import Shop
from shared.collison import point_in_poly
from shared.constants import VIEW_DISTANCE_SQ
from shared.gen.messages.v1 import (
    Activity,
    Interact,
    InteractStatus,
    InteractType,
    LoggedIn,
    Logout,
    ObjectAsset,
    Objects,
    ObjectType,
    Ping,
    SessionType,
    ShopInteract,
    User,
    Users,
)


class Game(Scene):
    def __init__(self, window: Window) -> None:
        super().__init__(window)
        self.batch = Batch()
        self.game_batch = Batch()
        self.frame = Frame(window, order=4)
        self.sound_manager = SoundManager()
        self.in_interaction_key = False
        # self.sound_manager.set_background_music("client/assets/determination.wav")
        # self.sound_manager.play_background_music()

        self.map = ClientMap()

        self.camera = CenteredCamera(window, None, None, scroll_speed=1)
        self.player: Player = Player()
        self.other_players: Dict[str, OtherPlayer] = {}
        self.npcs: Dict[str, NPC] = {}
        self.enemies: Dict[str, Enemy] = {}
        self.areas: Dict[str, Area] = {}
        self.pickupable: Dict[str, Pickupable] = {}

        self.input = InputScene(window=window)
        self.add_scene("input", self.input)

        self.dialog = DialogScene(window=window)
        self.add_scene("dialog", self.dialog)

        self.shop = Shop(window=window)
        self.add_scene("shop", self.shop)

        self.inventory = Inventory(window=window)
        self.add_scene("inventory", self.inventory)

        self.hud = Hud(window=window)
        self.add_scene("hud", self.hud)
        self.add_overlay_scene("hud")

        client.global_connection.ping_handler += self._on_ping
        client.global_connection.users_handler += self._on_users
        client.global_connection.logout_handler += self._on_player_logout
        client.global_connection.objects_handler += self._on_object_handler
        client.global_connection.login_handler += self._on_login_handler
        client.global_connection.interact_handler += self._on_interact_handler

    def remove_input(self) -> None:
        self.player.can_move = True

        if self.is_overlay_scene("input"):
            self.remove_overlay_scene("input")

        if not self.is_overlay_scene("hud"):
            self.add_overlay_scene("hud")

    def display_input(self, cb: Callable[[str], None] | None = None) -> None:
        self.player.can_move = False
        self.player.activity = Activity.ACTIVITY_IDLE

        self.input.callback = cb

        if self.is_overlay_scene("hud"):
            self.remove_overlay_scene("hud")

        if self.is_overlay_scene(scene_name="dialog"):
            self.remove_overlay_scene("dialog")

        self.add_overlay_scene("input")
        input_scene = cast(InputScene, self._sub_scenes["input"])
        input_scene.input._focus = True

    def remove_dialog(self) -> None:
        self.player.can_move = True

        if self.is_overlay_scene("dialog"):
            self.remove_overlay_scene("dialog")

        if not self.is_overlay_scene("hud"):
            self.add_overlay_scene("hud")

    def display_dialog(
        self, text: list[str], cb: Callable[[], None] | None = None
    ) -> None:
        self.player.can_move = False
        self.player.activity = Activity.ACTIVITY_IDLE

        self.dialog.callback = cb
        self.dialog.set_text(text)
        self.dialog.next_text()

        if self.is_overlay_scene("hud"):
            self.remove_overlay_scene("hud")
        if not self.is_overlay_scene("dialog"):
            self.add_overlay_scene("dialog")

        # self.dialog.start(text, cb=cb)

    def remove_shop(self) -> None:
        if self.shop.uuid in self.npcs:
            self.npcs[self.shop.uuid].stop_interaction()
        self.player.can_move = True

        if self.is_overlay_scene("shop"):
            self.remove_overlay_scene("shop")

        if not self.is_overlay_scene("hud"):
            self.add_overlay_scene("hud")

    def display_shop(
        self, items: list[ShopInteract], uuid: str, cb: Callable[[], None] | None = None
    ) -> None:
        self.player.can_move = False
        self.player.activity = Activity.ACTIVITY_IDLE
        self.shop.start(items, uuid, cb=cb)
        self.remove_overlay_scene("hud")
        self.add_overlay_scene("shop")

    def remove_inventory(self) -> None:
        self.player.can_move = True
        if self.is_overlay_scene("inventory"):
            self.remove_overlay_scene("inventory")

        if not self.is_overlay_scene("hud"):
            self.add_overlay_scene("hud")

    def display_inventory(self) -> None:
        if client.game_state.my_user is None:
            return

        self.player.can_move = False
        self.player.activity = Activity.ACTIVITY_IDLE
        self.inventory.set_inventory_items(client.game_state.my_user.inventory)

        self.remove_overlay_scene("hud")
        self.add_overlay_scene("inventory")

    def start_runner(self, uuid: str) -> None:
        client.scene_manager.set_scene(scene="dino_runner")
        runner = cast(DinoRunner, client.scene_manager._scenes["dino_runner"])
        runner.uuid = uuid

    def activate(self):
        if client.game_state.my_user:
            self.player.x = client.game_state.my_user.coords.x
            self.player.y = client.game_state.my_user.coords.y
            self.player._attacking = False

        for n in self.npcs.values():
            n.stop_interaction()

        self.in_interaction_key = False

        super().activate()

    def deactivate(self) -> None:
        super().deactivate()

    def _entity_in_view_distance(self, entity: ServerManagedEntity) -> bool:
        e = client.game_state.objects[entity.uuid][1]
        return (abs(self.player.x - e.coords.x) ** 2) + (
            abs(self.player.y - e.coords.y) ** 2
        ) <= VIEW_DISTANCE_SQ

    def _other_players_in_view_distance(self, entity: ServerManagedEntity) -> bool:
        e = client.game_state.users[entity.uuid]
        return (abs(self.player.x - e.coords.x) ** 2) + (
            abs(self.player.y - e.coords.y) ** 2
        ) <= VIEW_DISTANCE_SQ

    def draw(self) -> None:
        with self.camera:
            self.map.draw(self.camera)

            entities = chain(
                filter(
                    self._entity_in_view_distance,
                    chain(
                        self.npcs.values(),
                        self.enemies.values(),
                        self.pickupable.values(),
                    ),
                ),
                filter(
                    self._other_players_in_view_distance, self.other_players.values()
                ),
                [self.player],
            )
            for entity in sorted(entities, key=lambda entity: entity.y):
                entity.draw()

            self.game_batch.draw()

        self.batch.draw()

    def _on_interact_handler(self, interact: Interact) -> None:
        match interact.type:
            case InteractType.INTERACT_TYPE_TEXT:
                match interact.status:
                    case InteractStatus.INTERACT_STATUS_START:
                        npc = self.npcs[interact.uuid]
                        self.display_dialog([interact.text], cb=npc.interact)
                    case InteractStatus.INTERACT_STATUS_UPDATE:
                        if self.is_overlay_scene("dialog"):
                            self.dialog.append_text(interact.text)
                        else:
                            npc = self.npcs[interact.uuid]
                            self.display_dialog([interact.text], cb=npc.interact)
                    case InteractStatus.INTERACT_STATUS_STOP:
                        self.npcs[interact.uuid].stop_interaction()
                        self.remove_dialog()
                    case InteractStatus.INTERACT_STATUS_UNSPECIFIED:
                        assert False
            case InteractType.INTERACT_TYPE_RUNNER:
                match interact.status:
                    case InteractStatus.INTERACT_STATUS_START:
                        self.start_runner(interact.uuid)
                    case InteractStatus.INTERACT_STATUS_UPDATE:
                        print("RUNNER UPDATE")
                    case InteractStatus.INTERACT_STATUS_STOP:
                        print("RUNNER STOP")
                    case InteractStatus.INTERACT_STATUS_UNSPECIFIED:
                        assert False

            case InteractType.INTERACT_TYPE_SHOP:
                match interact.status:
                    case InteractStatus.INTERACT_STATUS_START:
                        npc = self.npcs[interact.uuid]
                        self.display_shop(interact.shop, interact.uuid, cb=npc.interact)
                    case InteractStatus.INTERACT_STATUS_UPDATE:
                        self.shop.set_shop_items(interact.shop, interact.uuid)
                    case InteractStatus.INTERACT_STATUS_STOP:
                        self.remove_shop()
                    case InteractStatus.INTERACT_STATUS_UNSPECIFIED:
                        assert False
            case InteractType.INTERACT_TYPE_CUT_OUT:
                match interact.status:
                    case InteractStatus.INTERACT_STATUS_START:
                        self.camera.cut_out = True
                    case InteractStatus.INTERACT_STATUS_UPDATE:
                        self.camera.cut_out = True
                    case InteractStatus.INTERACT_STATUS_STOP:
                        self.camera.cut_out = False
                    case InteractStatus.INTERACT_STATUS_UNSPECIFIED:
                        assert False
            case InteractType.INTERACT_TYPE_LICENSE:
                npc = self.npcs[interact.uuid]
                self.display_input(cb=npc.interact)
            case _:
                pass

    def _on_login_handler(self, login: LoggedIn) -> None:
        if login.success:
            self.player.interact_distance = login.interact_distance
            self.player.set_assets(login.assets)

        if login.type == SessionType.SESSION_TYPE_FREE_CAM:
            if self.is_overlay_scene("hud"):
                self.remove_overlay_scene("hud")

    def _on_object_asset_handler(self, object_asset: ObjectAsset) -> None:
        if object_asset.object_uuid in self.npcs:
            n = self.npcs[object_asset.object_uuid]

            assert (
                object_asset.type == ObjectType.OBJECT_TYPE_NPC
            ), "NOT IMPLEMENTED. Got: " + str(object_asset.type)

            n.label = object_asset.name
            n.interactable = object_asset.interactable
            n.interact_distance = object_asset.interact_distance
            n.set_assets(object_asset.assets)

        if object_asset.object_uuid in self.other_players:
            p = self.other_players[object_asset.object_uuid]

            p.set_assets(object_asset.assets)

        if object_asset.object_uuid in self.enemies:
            e = self.enemies[object_asset.object_uuid]

            assert (
                object_asset.type == ObjectType.OBJECT_TYPE_ENEMY
            ), "NOT IMPLEMENTED. Got: " + str(object_asset.type)

            e.set_assets(assets=object_asset.assets)

    def _on_object_handler(self, objects: Objects) -> None:
        for o in objects.objects:
            client.game_state.objects[o.uuid] = (
                client.game_state.objects[o.uuid][1]
                if o.uuid in client.game_state.objects
                else o,
                o,
            )

            if o.type == ObjectType.OBJECT_TYPE_UNSPECIFIED:
                pass  # Do nothing for now
            if o.type == ObjectType.OBJECT_TYPE_AREA:
                if o.remove:
                    del self.areas[o.uuid]
                else:
                    self.areas[o.uuid] = Area(o.uuid, o.area)
            elif o.type == ObjectType.OBJECT_TYPE_NPC:
                if o.remove and o.uuid not in self.npcs:
                    del self.npcs[o.uuid]
                elif o.uuid not in self.npcs:
                    self.npcs[o.uuid] = NPC(
                        uuid=o.uuid,
                        batch=self.game_batch,
                    )

                    client.global_connection.get_object_asset(
                        o.uuid, self._on_object_asset_handler
                    )
            elif o.type == ObjectType.OBJECT_TYPE_ENEMY:
                if o.remove and o.uuid in self.enemies:
                    del self.enemies[o.uuid]
                elif o.uuid not in self.enemies:
                    enemy_data = o.enemy_info
                    assert enemy_data is not None, "Enemy object without enemy data!"
                    self.enemies[o.uuid] = Enemy(
                        uuid=o.uuid,
                        health=enemy_data.health,
                        health_max=enemy_data.health_max,
                        batch=self.game_batch,
                        last_attack=enemy_data.last_attack,
                    )

                    client.global_connection.get_object_asset(
                        o.uuid, self._on_object_asset_handler
                    )
            elif o.type == ObjectType.OBJECT_TYPE_PICKUPABLE:
                if o.remove and o.uuid in self.pickupable:
                    del self.pickupable[o.uuid]
                elif o.uuid not in self.pickupable:
                    self.pickupable[o.uuid] = Pickupable(
                        uuid=o.uuid,
                        item=o.pickupable,
                        x=o.coords.x,
                        y=o.coords.y,
                    )

    def _on_player_logout(self, logout: Logout) -> None:
        if client.game_state.is_authenticated():
            if (
                client.game_state.my_user
                and logout.user.uuid == client.game_state.my_user.uuid
            ):
                self.logout()
            else:
                if logout.user.uuid in self.other_players:
                    del self.other_players[logout.user.uuid]

    def _on_ping(self, ping: Ping) -> None:
        client.game_state.last_ping = ping.time

    def _on_users(self, users: Users) -> None:
        u: Dict[str, User] = {user.uuid: user for user in users.users}

        if client.game_state.is_authenticated():
            if client.game_state.my_user:
                my_uuid = client.game_state.my_user.uuid
                if my_uuid in u:
                    coords = u[my_uuid].coords
                    self.player.x = coords.x
                    self.player.y = coords.y

                    client.game_state.my_user = u[my_uuid]

                    del u[my_uuid]

        new_players = u.keys() - self.other_players.keys()

        for uuid, user in u.items():
            if len(user.inventory) > 0:
                print(user.inventory)
            client.game_state.users[uuid] = user

        for new_player in new_players:
            self.other_players[new_player] = OtherPlayer(
                uuid=u[new_player].uuid,
                batch=self.game_batch,
            )

            client.global_connection.get_object_asset(
                u[new_player].uuid, self._on_object_asset_handler
            )

    def update(self, dt: float) -> None:
        online_time = datetime.now() - timedelta(minutes=1)
        if client.game_state.last_ping.timestamp() < online_time.timestamp():
            self.logout()

        self.player.update(dt)
        self.camera.position = (self.player.x, self.player.y)

        if self.player.coords_dirty:
            client.global_connection.move(
                self.player.x,
                self.player.y,
                self.player.rotation,
            )
            self.player.coords_dirty = False

        entities = chain(
            filter(
                self._entity_in_view_distance,
                chain(
                    self.npcs.values(),
                    self.enemies.values(),
                    self.pickupable.values(),
                ),
            ),
            filter(self._other_players_in_view_distance, self.other_players.values()),
        )

        for e in entities:
            e.update(dt)

        if (
            not client.game_state.my_user is None
            and client.game_state.my_user.health < 0
        ):
            client.global_connection.logout()
            client.game_state.logout()
            client.scene_manager.set_scene(scene="game_over")

        return super().update(dt)

    def on_key_release(self, symbol: int, modifiers: int) -> int | None:
        if symbol == SPACE:
            self.in_interaction_key = False

    def logout(self) -> None:
        client.global_connection.logout()
        client.game_state.logout()
        exit()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == ESCAPE:
            if self.shop in self._current_sub_scenes:
                self.remove_shop()
            elif self.inventory in self._current_sub_scenes:
                self.remove_inventory()
            else:
                self.logout()

            return EVENT_HANDLED

        if symbol == SPACE:
            if not self.in_interaction_key:
                try:
                    if self.is_overlay_scene("dialog"):
                        self.dialog.next_text()
                        return

                    if self.is_overlay_scene("input"):
                        return

                    for npc in self.npcs.values():
                        if not npc.interactable:
                            continue

                        dx = (self.player.x + self.player.interact_offset[0]) - (
                            (npc.x + npc.interact_offset[0])
                        )
                        dy = (self.player.y + self.player.interact_offset[1]) - (
                            (npc.y + npc.interact_offset[1])
                        )
                        distance_sq = dx**2 + dy**2
                        if (
                            distance_sq
                            < (npc.interact_distance + self.player.interact_distance)
                            ** 2
                        ):
                            npc.interact()
                            return

                    # check for area collision
                    for area in self.areas.values():
                        if point_in_poly(self.player.x, self.player.y, area.area):
                            area.interact()

                finally:
                    self.in_interaction_key = True

    def buy(self, item: ShopInteract) -> None:
        npc = self.npcs[self.shop.uuid]
        npc.in_interaction = False

        client.global_connection.interact(
            uuid=self.shop.uuid,
            status=InteractStatus.INTERACT_STATUS_UPDATE,
            shop=[item],
        )

        self.remove_shop()
