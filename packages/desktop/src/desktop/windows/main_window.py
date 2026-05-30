import customtkinter as ctk
from desktop.widgets import StatusBar, MenuBar, InstanceSelector


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.minsize(350, 200)
        self.title("Astra Launcher")

        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x")

        self.menu_bar = MenuBar(self)
        self.menu_bar.pack(side="top", fill="x")

        self.instance_selector = InstanceSelector(
            self, status_bar=self.status_bar, fg_color="transparent"
        )
        self.instance_selector.pack(
            side="top", fill="both", expand=True, padx=10, pady=10
        )
