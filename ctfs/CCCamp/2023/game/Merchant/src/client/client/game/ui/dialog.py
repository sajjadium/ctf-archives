from typing import Callable, cast

from pyglet import clock
from pyglet.graphics import Batch
from pyglet.gui.widgets import WidgetBase
from pyglet.image import Texture
from pyglet.text.document import FormattedDocument
from pyglet.text.layout import TextLayout, _Line  # pyright: ignore[reportPrivateUsage]

from client.game.nearest_sprite import NearestSprite
from client.game.ui import get_ui_grid
from client.game.ui.tilebox import TileBox

DialogCallback = Callable[[], None] | None


class Dialog(WidgetBase):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: list[str],
        batch: Batch,
        cb: DialogCallback = None,
    ) -> None:
        self.text = text
        self._outline = TileBox(x, y, width, height)
        offset = self._outline.tile_size
        self.inner_width = (width // self._outline.tile_size) * self._outline.tile_size
        self.inner_height = (
            height // self._outline.tile_size
        ) * self._outline.tile_size

        self.text_idx = 0
        self.document = FormattedDocument("")
        self.flow_document = FormattedDocument("")
        self.flow_document_layout = TextLayout(
            height=self.inner_height - offset * 2,
            width=self.inner_width - offset * 2,
            document=self.flow_document,
            multiline=True,
        )
        self.flow_document_layout.visible = False
        self.flow_document_layout.x = x + offset
        self.flow_document_layout.y = y + offset
        self._layout = TextLayout(
            height=self.inner_height - offset * 2,
            width=self.inner_width - offset * 2,
            batch=batch,
            document=self.document,
            multiline=True,
        )
        self._layout.x = x + offset
        self._layout.y = y + offset
        self._blink = NearestSprite(
            cast(Texture, get_ui_grid()[23]),
            x=x + self.inner_width - offset - cast(int, get_ui_grid().item_width) - 4,
            y=y + offset,
            origin=(
                cast(int, get_ui_grid().item_width) // 2,
                cast(int, get_ui_grid().item_height) // 2,
            ),
        )
        self._blink.scale = 2.2
        self._blink.visible = False
        self._pressed = False
        self._wait_for_next_page = True
        self._char_idx = 0
        self.PERIOD = 0.01  # in s
        self.BLINK_PERIOD = 0.5
        self.cb = cb
        clock.schedule_interval(self._do_blink, self.BLINK_PERIOD)
        super().__init__(x, y, width, height)
        self.enabled = len(self.text) != 0

        self.dirty = True

    def _do_blink(self, dt: float) -> None:
        if not self.enabled:
            return
        self._blink.visible = not self._blink.visible

    def draw(self) -> None:
        if not self.enabled:
            return

        if self.dirty:
            self.next_text()
            self.dirty = False

        self._outline.draw()
        self._blink.draw()

    def _next_char(self, dt: float) -> None:
        if not self.enabled:
            return

        if len(self.text) == 0:
            return

        # Breaks if text start with a space
        if self.text[self.text_idx][self._char_idx] == " ":
            # check if next word would wrap
            # get next word
            next_word = self.text[self.text_idx][self._char_idx + 1 :].split(" ")[0]
            self.flow_document.text = self.document.text + " " + next_word
            flow_lines = cast(
                list[_Line],
                self.flow_document_layout._get_lines(),  # pyright: ignore[reportPrivateUsage]
            )
            layout_lines = cast(
                list[_Line],
                self._layout._get_lines(),  # pyright: ignore[reportPrivateUsage]
            )
            if len(flow_lines) > len(layout_lines):
                # would wrap insert newline
                self.document.insert_text(
                    len(self.document.text), "\n", {"color": (255, 255, 255, 255)}
                )
                # skip whitespace
                self._char_idx += 1
                if cast(int, self.flow_document_layout.content_height) > cast(
                    int, self.flow_document_layout.height
                ):
                    self._wait_for_next_page = True
                    clock.unschedule(self._next_char)
                    clock.schedule_interval(self._do_blink, self.BLINK_PERIOD)
                    self._blink.visible = True

        if not self._wait_for_next_page:
            self.document.insert_text(
                len(self.document.text),
                self.text[self.text_idx][self._char_idx],
                {"color": (0, 0, 0, 255)},
            )
            self._char_idx += 1
            if self._char_idx >= len(self.text[self.text_idx]):
                clock.unschedule(self._next_char)
                clock.schedule_interval(self._do_blink, self.BLINK_PERIOD)
                self.text_idx += 1
                self._char_idx = 0
                self._blink.visible = True

    def next_text(self) -> None:
        if not self.enabled:
            return

        self._blink.visible = False
        clock.unschedule(self._do_blink)
        if self._wait_for_next_page:
            self._wait_for_next_page = False
            self.document.text = ""
            self.flow_document.text = ""
            clock.schedule_interval(self._next_char, self.PERIOD)
            return
        clock.unschedule(self._next_char)
        if self.text_idx >= len(self.text):
            if self.cb:
                self.cb()

            return
        if self.text_idx != 0:
            self.document.insert_text(
                len(self.document.text), " ", {"color": (255, 255, 255, 255)}
            )
        clock.schedule_interval(self._next_char, self.PERIOD)

    def on_mouse_press(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled or not self._check_hit(x, y):
            return
        if not self._pressed:
            self.next_text()
        self._pressed = True

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled or not self._pressed:
            return
        self._pressed = False

    def append_text(self, text: str) -> None:
        self.reset()
        self.text.append(text)

        self.dirty = True

    def start(self, text: list[str], cb: DialogCallback = None) -> None:
        self.text = text
        self.enabled = True
        self.cb = cb

        self.next_text()

    def stop(self) -> None:
        self.reset()

        self.enabled = False
        self.cb = None

    def reset(self) -> None:
        self.text = []

        self.document.text = ""
        self.flow_document.text = ""
        self._blink.visible = False
        self._pressed = False
        self._wait_for_next_page = True
        self._char_idx = 0
        self.text_idx = 0
