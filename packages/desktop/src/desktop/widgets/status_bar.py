import customtkinter as ctk


class StatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=30, corner_radius=0, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.status_label = ctk.CTkLabel(self, text="", anchor="w", padx=10)
        self.status_label.grid(row=0, column=0, sticky="ew")

        self.author_label = ctk.CTkLabel(
            self, text="Author: kotop21", anchor="e", padx=10
        )
        self.author_label.grid(row=0, column=1, sticky="e")

    def set_status(self, text: str):
        self.status_label.configure(text=text)
