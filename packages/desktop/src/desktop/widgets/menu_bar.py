import warnings
import customtkinter as ctk
from typing import Callable, Optional
from ttkbootstrap_icons_lucide import LucideIcon
from desktop.components import SmartButton

warnings.filterwarnings("ignore", category=UserWarning, module="customtkinter")


class MenuBar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_add_server: Optional[Callable] = None,
        on_folders: Optional[Callable] = None,
        on_settings: Optional[Callable] = None,
        on_help: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(master, height=50, corner_radius=0, **kwargs)

        self.pack_propagate(False)

        icon_size = 32
        icon_color = "#FFFFFF"

        self.icon_add = LucideIcon(
            "circle-plus", size=icon_size, color=icon_color
        ).image
        self.icon_folders = LucideIcon("folder", size=icon_size, color=icon_color).image
        self.icon_settings = LucideIcon(
            "settings", size=icon_size, color=icon_color
        ).image
        self.icon_help = LucideIcon(
            "circle-help", size=icon_size, color=icon_color
        ).image

        status_bar = getattr(master, "status_bar", None)

        btn_kwargs = {
            "fg_color": "transparent",
            "master": self,
            "height": 32,
            "compound": "left",
            "anchor": "w",
            "status_bar": status_bar,
        }

        from desktop.windows import SettingsWindow, AddServerWindow

        self.btn_add = SmartButton(
            text="Add server",
            width=130,
            image=self.icon_add,
            window_class=AddServerWindow,
            hover_text="Add a new server",
            **btn_kwargs,
        )
        self.btn_add.pack(side="left", padx=5, pady=9)

        self.btn_folders = SmartButton(
            text="Folders",
            width=90,
            image=self.icon_folders,
            command=on_folders,
            hover_text="Open server directories",
            **btn_kwargs,
        )
        self.btn_folders.pack(side="left", padx=5, pady=9)

        self.btn_settings = SmartButton(
            text="Settings",
            width=110,
            image=self.icon_settings,
            window_class=SettingsWindow,
            hover_text="Global launcher settings",
            **btn_kwargs,
        )
        self.btn_settings.pack(side="left", padx=5, pady=9)

        self.btn_help = SmartButton(
            text="Help",
            width=90,
            image=self.icon_help,
            command=on_help,
            hover_text="Documentation and support",
            **btn_kwargs,
        )
        self.btn_help.pack(side="left", padx=5, pady=9)
