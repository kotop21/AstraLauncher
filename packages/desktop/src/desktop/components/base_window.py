import re

import customtkinter as ctk
from core.app_config import config


class BaseWindow(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        title="Launcher",
        size=(800, 600),
        window_key=None,
        resizable=(False, False),
        **kwargs,
    ):
        root_master = parent.winfo_toplevel() if parent else None
        super().__init__(master=root_master, **kwargs)

        self.title(title)
        self.resizable(resizable[0], resizable[1])
        self._window_key = window_key

        saved_geometry = (
            config.get(f"{self._window_key}_geometry") if self._window_key else None
        )

        is_valid_geom = False
        if saved_geometry and isinstance(saved_geometry, str):
            match = re.match(r"^(\d+)x(\d+)([-+]\d+)([-+]\d+)$", saved_geometry)
            if match:
                w, h, x, y = map(int, match.groups())
                screen_w = self.winfo_screenwidth()
                screen_h = self.winfo_screenheight()
                if (
                    w >= 200
                    and h >= 200
                    and (x + w > 50)
                    and (x < screen_w - 50)
                    and (y + h > 50)
                    and (y < screen_h - 50)
                ):
                    is_valid_geom = True

        if is_valid_geom and isinstance(saved_geometry, str):
            self.geometry(saved_geometry)
        else:
            self.update_idletasks()
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            x = max(0, (screen_w // 2) - (size[0] // 2))
            y = max(0, (screen_h // 2) - (size[1] // 2))
            self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

        self.after(100, self.lift)
        self.after(150, self.focus_force)

        self.protocol("WM_DELETE_WINDOW", self._internal_on_close)

    def _internal_on_close(self):
        if self._window_key:
            config.set(f"{self._window_key}_geometry", self.geometry())
        self.on_close()

    def on_close(self):
        self.destroy()
