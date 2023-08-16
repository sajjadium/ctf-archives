import inspect
from typing import Any, cast

import pyperclip
from pyglet.graphics import Batch, Group
from pyglet.gui import TextEntry
from pyglet.text.document import AbstractDocument
from pyglet.window.key import MOTION_COPY, MOTION_PASTE

from client import MOTION_DELETE_REST, MOTION_SELECT_ALL
from client.game.ui.tilebox import TileStrip


class AdvancedTextEntry(TextEntry):
    def on_text_motion(self, motion: int):
        handled = False
        if self._focus:
            handled = True
            doc = cast(AbstractDocument, self._layout.document)
            caret_doc = cast(
                AbstractDocument,
                self._caret._layout.document,  # pyright: ignore[reportPrivateUsage]
            )
            match motion:
                case MOTION_COPY.real:
                    selected_text = (
                        doc.text[
                            self._layout._selection_start : self._layout._selection_end  # pyright: ignore[reportPrivateUsage]
                        ],
                    )

                    pyperclip.copy(selected_text)
                case MOTION_PASTE.real:
                    self.on_text(pyperclip.paste())
                case MOTION_SELECT_ALL.real:
                    self._caret.position = 0
                    self._caret.mark = len(doc.text)
                    self._layout.set_selection(0, len(doc.text))
                case MOTION_DELETE_REST.real:
                    w = self._caret._next_word_re.search(  # pyright: ignore[reportPrivateUsage]
                        caret_doc.text,
                        cast(
                            int,
                            self._caret._position,  # pyright: ignore[reportPrivateUsage]
                        ),
                    )
                    caret_doc.delete_text(
                        cast(
                            int,
                            self._caret._position,  # pyright: ignore[reportPrivateUsage]
                        ),
                        w.endpos if w else len(doc.text),
                    )
                case _:
                    handled = False
        if not handled:
            super().on_text_motion(motion)


class TextInput(AdvancedTextEntry):
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        color: tuple[int, int, int, int] = ...,
        text_color: tuple[int, int, int, int] = ...,
        caret_color: tuple[int, int, int, int] = ...,
        batch: Batch | None = None,
        group: Group | None = None,
    ):
        self.bg = TileStrip(
            x - 13 * 2,
            y - 8,
            width + 13 * 2,
            32,
            32,
            3,
            23,
            group=group,
        )
        super().__init__(
            text,
            x + 13,
            y,
            width - 32,
            color,
            text_color,
            caret_color,
            batch,
            group,
        )

    def draw(self):
        self.bg.draw()


class Proxy:
    wrap: AbstractDocument

    def __init__(self, wrap: AbstractDocument):
        self.__dict__["wrap"] = wrap

    def __getattr__(self, name: str):
        if name == "text":
            stack = inspect.stack()
            if stack[1][0].f_code.co_name == "on_text":
                return getattr(self.wrap, name)
            return "*" * len(getattr(self.wrap, name))
        return getattr(self.wrap, name)

    def __setattr__(self, name: str, value: Any):
        setattr(self.wrap, name, value)


class PasswordInput(TextInput):
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        color: tuple[int, int, int, int] = ...,
        text_color: tuple[int, int, int, int] = ...,
        caret_color: tuple[int, int, int, int] = ...,
        batch: Batch | None = None,
        group: Group | None = None,
    ):
        super().__init__(
            text, x, y, width, color, text_color, caret_color, batch, group
        )
        self._layout.document = Proxy(cast(AbstractDocument, self._layout.document))
