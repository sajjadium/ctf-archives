from pathlib import Path
from typing import cast

from pyglet import image
from pyglet.graphics import Batch
from pyglet.gui import Frame
from pyglet.image import ImageData
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import Window

import client
from client.game.ui.button import TextButton
from client.game.ui.input import PasswordInput, TextInput
from client.scenes.scenemanager import Scene
from shared.gen.messages.v1 import ErrorType, LoggedIn


class MainMenu(Scene):
    status: str

    def get_background_image(self) -> ImageData:
        return cast(
            ImageData,
            image.load(Path(client.PATH, "assets/main_menu_background.png")),
        )

    def __init__(self, window: Window, username: str, password: str) -> None:
        super().__init__(window)

        self.frame = Frame(window, order=4)
        self.batch = Batch()
        self.status = ""

        self.background_image = self.get_background_image()
        self.background = Sprite(img=self.background_image, x=0, y=-70)

        self.game_logo = Sprite(
            img=image.load(Path(client.PATH, "assets/game_logo.gif")),
            x=50,
            y=250,
            batch=self.batch,
        )

        self.game_logo.width = 900
        self.game_logo.height = 314

        self.username_label = Label(
            "Username", x=300, y=250, batch=self.batch, color=(75, 20, 78, 255)
        )
        self._input_username = TextInput(
            text=username,
            x=300,
            y=225,
            width=200,
            batch=self.batch,
            text_color=(0, 0, 0, 255),
            caret_color=(0, 0, 0, 255),
            color=(0, 0, 0, 0),
        )

        self.password_label = Label(
            "Password", x=300, y=200, batch=self.batch, color=(0, 0, 0, 255)
        )
        self._input_password = PasswordInput(
            text=password,
            x=300,
            y=175,
            width=200,
            batch=self.batch,
            text_color=(0, 0, 0, 255),
            caret_color=(0, 0, 0, 255),
            color=(0, 0, 0, 0),
        )

        self.status_label = Label(
            self.status, x=300, y=140, batch=self.batch, color=(255, 0, 0, 255)
        )

        def login():
            def login_sucess(l: LoggedIn) -> None:
                if l.success:
                    client.scene_manager.set_scene("game")
                else:
                    match l.error:
                        case ErrorType.ERROR_TYPE_UNAUTHORIZED:
                            self.status = "Username or Password doesn't match"
                        case ErrorType.ERROR_TYPE_TIMEOUT:
                            self.status = f"You died and are still in the timeout phase"
                        case ErrorType.ERROR_TYPE_UNSPECIFIED:
                            self.status = "Unknown error"
                        case ErrorType.ERROR_TYPE_ALREADY_LOGGED_IN:
                            self.status = "User already logged in elsewhere or crashed not too long ago."
                        case _:
                            self.status = "Unknown error"

            username = self._input_username.value
            password = self._input_password.value

            client.global_connection.login(
                username=username, password=password, handler=login_sucess
            )

        self._text_button = TextButton("Login", x=300, y=70, batch=self.batch)
        self._text_button.set_handler("on_press", login)

    def activate(self) -> None:
        self.window.push_handlers(self._input_password)
        self.window.push_handlers(self._input_username)
        self.frame.add_widget(self._text_button)

        super().activate()

    def deactivate(self) -> None:
        self.window.remove_handlers(self._input_password)
        self.window.remove_handlers(self._input_username)
        self.frame.remove_widget(self._text_button)

        super().deactivate()

    def draw(self) -> None:
        self.background.draw()
        self._text_button.draw()
        self._input_password.draw()
        self._input_username.draw()
        self.batch.draw()

    def update(self, dt: float) -> None:
        self.status_label.text = self.status
