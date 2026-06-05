import tkinter as tk

import customtkinter as ctk
from desktop.components import SmartButton
from ttkbootstrap_icons_lucide import LucideIcon

from .menu_bar_actions import MenuBarActions


class MenuBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=50, corner_radius=0, **kwargs)

        self.pack_propagate(False)
        self.actions = MenuBarActions(self)

        theme_colors = ctk.ThemeManager.theme["CTkLabel"]["text_color"]
        light_col = theme_colors[0] if isinstance(theme_colors, list) else "black"
        dark_col = theme_colors[1] if isinstance(theme_colors, list) else "white"

        icon_size = 32

        self.icon_add = self._create_icon("circle-plus", icon_size, light_col, dark_col)
        self.icon_folders = self._create_icon("folder", icon_size, light_col, dark_col)
        self.icon_settings = self._create_icon(
            "settings", icon_size, light_col, dark_col
        )
        self.icon_help = self._create_icon(
            "circle-help", icon_size, light_col, dark_col
        )

        status_bar = getattr(master, "status_bar", None)

        btn_kwargs = {
            "fg_color": "transparent",
            "text_color": theme_colors,
            "master": self,
            "height": 32,
            "compound": "left",
            "anchor": "w",
            "status_bar": status_bar,
        }

        from desktop.windows import AddServerWindow

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
            command=self._show_folders_menu,
            hover_text="Open server directories",
            **btn_kwargs,
        )
        self.btn_folders.pack(side="left", padx=5, pady=9)

        self.btn_help = SmartButton(
            text="Help",
            width=90,
            image=self.icon_help,
            command=self._show_help_menu,
            hover_text="Documentation and support",
            **btn_kwargs,
        )
        self.btn_help.pack(side="left", padx=5, pady=9)

    def _create_icon(self, name, size, light_color, dark_color):
        """Создает CTkImage с поддержкой смены тем (Светлая/Темная)."""
        img_light = LucideIcon(name, size=size, color=light_color).image
        img_dark = LucideIcon(name, size=size, color=dark_color).image
        return ctk.CTkImage(
            light_image=img_light, dark_image=img_dark, size=(size, size)
        )

    def _show_folders_menu(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(
            label="All servers folder",
            command=self.actions.open_all_servers_folder,
        )
        menu.add_command(
            label="Launcher directory",
            command=self.actions.open_launcher_folder,
        )

        x = self.btn_folders.winfo_rootx()
        y = self.btn_folders.winfo_rooty() + self.btn_folders.winfo_height()
        menu.post(x, y)

    def _show_help_menu(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(
            label="Open launcher repository",
            command=self.actions.open_repository,
        )
        menu.add_command(
            label="Support the developer",
            command=self.actions.support_developer,
        )
        menu.add_command(
            label="Report an issue / suggest a feature",
            command=self.actions.report_issue,
        )

        x = self.btn_help.winfo_rootx()
        y = self.btn_help.winfo_rooty() + self.btn_help.winfo_height()
        menu.post(x, y)
