from __future__ import annotations

import time
from abc import ABC, abstractmethod

from pyglet.input import Controller, ControllerManager
from pyglet.window import Window, key

import client
from shared.constants import TARGET_FPS, TARGET_UPS


class Scene(ABC):
    _sub_scenes: dict[str, Scene]
    _current_sub_scenes: list[Scene]

    _tmp_new_sub_scenes: list[Scene]
    _tmp_old_sub_scenes: list[Scene]

    def __init__(self, window: Window) -> None:
        self.window = window

        self._sub_scenes = {}
        self._current_sub_scenes = []
        self._tmp_new_sub_scenes = []
        self._tmp_old_sub_scenes = []

    def inner_draw(self) -> None:
        if len(self._tmp_new_sub_scenes) > 0:
            for scene in self._tmp_new_sub_scenes:
                if scene not in self._current_sub_scenes:
                    self._current_sub_scenes.append(scene)
                    scene.activate()

            self._tmp_new_sub_scenes.clear()

        if len(self._tmp_old_sub_scenes) > 0:
            for scene in self._tmp_old_sub_scenes:
                if scene in self._current_sub_scenes:
                    self._current_sub_scenes.remove(scene)
                    scene.deactivate()

            self._tmp_old_sub_scenes.clear()

        self.draw()

        for scene in self._current_sub_scenes:
            scene.inner_draw()

    @abstractmethod
    def draw(self) -> None:
        pass

    def activate(self) -> None:
        for scene in self._current_sub_scenes:
            self.window.push_handlers(scene)

            scene.activate()

    def deactivate(self) -> None:
        for scene in self._current_sub_scenes:
            self.window.remove_handlers(scene)

            scene.deactivate()

    def update(self, dt: float) -> None:
        for scene in self._current_sub_scenes:
            scene.update(dt)

    # Controller event handlers:
    def on_dpad_motion(
        self,
        controller: Controller,
        dpleft: bool,
        dpright: bool,
        dpup: bool,
        dpdown: bool,
    ) -> None:
        pass

    def on_button_press(self, controller: Controller, button: str) -> int | None:
        pass

    def on_button_release(self, controller: Controller, button: str) -> int | None:
        pass

    def on_stick_motion(
        self, controller: Controller, stick: str, xvalue: float, yvalue: float
    ) -> int | None:
        pass

    # Keyboard event handlers:
    def on_key_press(self, symbol: int, modifiers: int) -> int | None:
        pass

    def on_key_release(self, symbol: int, modifiers: int) -> int | None:
        pass

    def add_scene(self, name: str, scene: Scene) -> None:
        self._sub_scenes[name] = scene

    def remove_scene(self, name: str) -> None:
        del self._sub_scenes[name]

    def is_overlay_scene(self, scene_name: str) -> bool:
        scene = self._sub_scenes[scene_name]

        return scene in self._current_sub_scenes or scene in self._tmp_new_sub_scenes

    def add_overlay_scene(self, scene_name: str) -> None:
        assert scene_name in self._sub_scenes, "Sub Scene not found! Did you add it?"

        scene = self._sub_scenes[scene_name]

        self.window.push_handlers(scene)

        self._tmp_new_sub_scenes.append(scene)

    def remove_overlay_scene(self, scene_name: str) -> None:
        assert scene_name in self._sub_scenes, "Sub Scene not found! Did you add it?"

        assert self.is_overlay_scene(scene_name), "Sub Scene not activated!"

        scene = self._sub_scenes[scene_name]
        if scene in self._current_sub_scenes:
            self.window.remove_handlers(scene)

            self._tmp_old_sub_scenes.append(scene)

        if scene in self._tmp_new_sub_scenes:
            self._tmp_new_sub_scenes.remove(scene)


class StubScene(Scene):
    def draw(self) -> None:
        pass


class SceneManager:
    window: Window
    current_scene: Scene | None
    overlay_scene: Scene | None
    _scenes: dict[str, Scene]

    _tmp_scene: str | None
    _tmp_overlay_scene: str | None

    def __init__(self, window: Window) -> None:
        self.window = window
        self.window.on_draw = self._on_draw
        self.stats = []

        self._scenes = {}
        self.current_scene = None
        self.overlay_scene = None
        self._tmp_scene = None
        self._tmp_overlay_scene = None
        self.last_draw = None
        self.last_update = None

        # Instantiation a ControllerManager to handle hot-plugging:
        self.controller = None
        self.controller_manager = ControllerManager()
        self.controller_manager.on_connect = self.on_controller_connect
        self.controller_manager.on_disconnect = self.on_controller_disconnect

        # Initialize Controller if it's connected:
        controllers: list[Controller] = self.controller_manager.get_controllers()
        if controllers:
            self.on_controller_connect(controllers[0])

        # Initialize Keystate helper
        self.keys = key.KeyStateHandler()
        window.push_handlers(self.keys)

    def _on_draw(self) -> None:
        with client.game_state.draw_lock:
            a = time.time()
            # if self.last_draw:
            # if 1 / (a - self.last_draw) < ((TARGET_FPS) * 0.7):
            # tracer = get_tracer()
            # if tracer:
            #    tracer.log_instant("LAAAAG", 1 / (a - self.last_draw), scope="g")
            # print("LAAAAG", 1 / (a - self.last_draw))
            # for stat in self.stats:
            #    print(stat)
            if self._tmp_scene:
                self._set_scene()

            if self._tmp_overlay_scene:
                self._set_overlay_scene()

            self.window.clear()
            if self.current_scene:
                self.current_scene.inner_draw()
            if self.overlay_scene:
                self.overlay_scene.inner_draw()
            self.last_draw = time.time()
            dt = self.last_draw - a
            # print(dt)
            if dt > 1 / (TARGET_FPS * 0.9):
                # if get_tracer():
                #     get_tracer().log_instant("Frame long draw", dt, scope="g")

                print("frame took too long to draw :(", dt)

    def on_controller_connect(self, controller: Controller) -> None:
        if not self.controller:
            controller.open()
            self.controller = controller
            self.controller.push_handlers(self.current_scene)
            self.controller.push_handlers(self.overlay_scene)
        else:
            print(f"A Controller is already connected: {self.controller}")

    def on_controller_disconnect(self, controller: Controller) -> None:
        if self.controller and self.controller == controller:
            self.controller.remove_handlers(self.current_scene)
            self.controller.remove_handlers(self.overlay_scene)

            self.controller = None

    def add_scene(self, name: str, scene: Scene) -> None:
        self._scenes[name] = scene

    def _set_scene(self) -> None:
        if self.current_scene:
            self.current_scene.deactivate()
            self.window.remove_handlers(self.current_scene)
            if self.controller:
                self.controller.remove_handlers(self.current_scene)
        if not self._tmp_scene:
            self.current_scene = None
            return
        assert self._tmp_scene in self._scenes, "Scene not found! Did you add it?"

        self.current_scene = self._scenes[self._tmp_scene]
        self.current_scene.activate()
        self.window.push_handlers(self.current_scene)
        if self.controller:
            self.controller.push_handlers(self.current_scene)

        self._tmp_scene = None

    def set_scene(self, scene: str | None) -> None:
        if scene:
            self._tmp_scene = scene
        else:
            self._tmp_scene = ""

    def _set_overlay_scene(self) -> None:
        if self.overlay_scene:
            self.overlay_scene.deactivate()
            self.window.remove_handlers(self.overlay_scene)
            if self.controller:
                self.controller.remove_handlers(self.overlay_scene)

        if self._tmp_overlay_scene is None:
            self.overlay_scene = self._tmp_overlay_scene
            return
        assert (
            self._tmp_overlay_scene in self._scenes
        ), "Scene not found! Did you add it?"

        self.overlay_scene = self._scenes[self._tmp_overlay_scene]
        self.overlay_scene.activate()
        self.window.push_handlers(self.overlay_scene)
        if self.controller:
            self.controller.push_handlers(self.overlay_scene)

        self._tmp_overlay_scene = None

    def set_overlay_scene(self, scene: str | None) -> None:
        if scene:
            self._tmp_overlay_scene = scene
        else:
            self._tmp_overlay_scene = ""

    def update(self, dt: float) -> None:
        with client.game_state.update_lock:
            a = time.time()
            # if self.last_update:
            #     divider = a - self.last_update
            #     if divider > 1 / (TARGET_UPS * 0.5):
            #         print("UPS LAAAAG", divider)
            # for stat in self.stats:
            #    print(stat)
            if self.current_scene:
                self.current_scene.update(dt)
            if self.overlay_scene:
                self.overlay_scene.update(dt)
            self.last_update = time.time()
            dt = self.last_update - a
            # print(dt)
            if dt > 1 / (TARGET_UPS * 0.9):
                # if get_tracer():
                #     get_tracer().log_instant("Frame long draw", dt, scope="g")

                print("update took too long to process :(", dt)
