from typing import cast

from pyglet.graphics import Batch, Group
from pyglet.gui.widgets import WidgetBase
from pyglet.shapes import Rectangle
from pyglet.text import Label


class DropdownEntry(WidgetBase):
    def __init__(self, x: int, y: int, text: str, batch: Batch, group: Group):
        padding = 0
        self._label = Label(
            text,
            x=x + padding,
            y=y + padding,
            batch=batch,
            anchor_y="bottom",
            color=(255, 255, 255, 255),
            group=group,
        )
        label_width = self._label.content_width
        label_height = cast(int, self._label.content_height)
        width = label_width + padding * 2
        height = label_height + padding * 2
        super().__init__(x, y, width, height)


class Dropdown(WidgetBase):
    def __init__(
        self,
        x: int,
        y: int,
        entries: list[str],
        batch: Batch,
    ) -> None:
        self.group = Group()
        self.entries: list[DropdownEntry] = []
        height = 0
        width = 0
        for entry in entries[::-1]:
            dentry = DropdownEntry(
                x=x, y=y + height, text=entry, batch=batch, group=self.group
            )
            height += dentry.height
            width = max(width, dentry.width)
            self.entries.append(dentry)
        self._outline = Rectangle(
            x, y, width, height, color=(80, 0, 80, 255), batch=batch
        )
        self._selector = Rectangle(
            x, y, width, 0, color=(255, 255, 255, 255), batch=batch
        )
        self._selector.opacity = 0
        self.selected_entry = None
        super().__init__(x, y, width, height)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        if self._check_hit(x, y):
            for entry in self.entries:
                if entry.y < y < entry.y + entry.height:
                    break
            else:
                self._selector.opacity = 0
                if self.selected_entry:
                    self.selected_entry._label.color = (  # pyright: ignore[reportPrivateUsage]
                        255,
                        255,
                        255,
                        255,
                    )
                self.selected_entry = None
                return
            self._selector.x = entry.x
            self._selector.y = entry.y
            self._selector.height = entry.height
            self._selector.opacity = 255
            if self.selected_entry:
                self.selected_entry._label.color = (  # pyright: ignore[reportPrivateUsage]
                    255,
                    255,
                    255,
                    255,
                )
            entry._label.color = (0, 0, 0, 255)  # pyright: ignore[reportPrivateUsage]
            self.selected_entry = entry
