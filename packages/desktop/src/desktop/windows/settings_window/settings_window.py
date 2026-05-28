import customtkinter as ctk
from desktop.components import BaseWindow


class SettingsWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, title="Settings", size=(500, 400))

        self.label_main = ctk.CTkLabel(
            self, text="Global Configuration", font=("", 20, "bold")
        )
        self.label_main.pack(pady=(20, 20), padx=20, anchor="w")

        self.btn_theme = ctk.CTkButton(self, text="Toggle Dark Mode")
        self.btn_theme.pack(pady=10, padx=20, anchor="w")

        self.btn_clear = ctk.CTkButton(self, text="Clear Cache", fg_color="red")
        self.btn_clear.pack(pady=10, padx=20, anchor="w")
