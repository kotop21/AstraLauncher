import customtkinter as ctk
from desktop.widgets import StatusBar, MenuBar, InstanceSelector


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.minsize(600, 200)
        self.title("Serv Launcher")

        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x")

        self.menu_bar = MenuBar(
            self,
            on_add_server=self.action_add_server,
            on_folders=self.action_open_folders,
            on_help=self.action_open_help,
        )
        self.menu_bar.pack(side="top", fill="x")

        self.instance_selector = InstanceSelector(
            self, status_bar=self.status_bar, fg_color="transparent"
        )
        self.instance_selector.pack(
            side="top", fill="both", expand=True, padx=10, pady=10
        )

    def action_add_server(self):
        print("Button pressed: add_server")

    def action_open_folders(self):
        print("Button pressed: open_folders")

    def action_open_help(self):
        print("Button pressed: open_help")
