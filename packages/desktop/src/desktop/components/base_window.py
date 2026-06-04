import customtkinter as ctk


class BaseWindow(ctk.CTkToplevel):
    def __init__(
        self, parent, title="Launcher", size=(800, 600), saved_geometry=None, **kwargs
    ):
        super().__init__(master=parent, **kwargs)
        self.title(title)
        self.resizable(False, False)

        self.withdraw()
        self.update_idletasks()

        if saved_geometry and "+-" not in saved_geometry and "-+" not in saved_geometry:
            self.geometry(saved_geometry)
        else:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            x = (screen_w // 2) - (size[0] // 2)
            y = (screen_h // 2) - (size[1] // 2)
            self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

        self.deiconify()
        self.focus()
