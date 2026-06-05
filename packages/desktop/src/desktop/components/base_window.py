import logging
import traceback

import customtkinter as ctk


class BaseWindow(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        title="Launcher",
        size=(800, 600),
        resizable=(False, False),
        transient_to_parent=True,
        window_key=None,
        **kwargs,
    ):
        root_master = parent.winfo_toplevel() if parent else None
        super().__init__(master=root_master, **kwargs)

        self.withdraw()

        if root_master and transient_to_parent:
            self.transient(root_master)

        self.title(title)
        self.resizable(resizable[0], resizable[1])

        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = max(0, (screen_w // 2) - (size[0] // 2))
        y = max(0, (screen_h // 2) - (size[1] // 2))
        self.geometry(f"{size[0]}x{size[1]}+{int(x)}+{int(y)}")

        self.deiconify()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        logging.info(
            f"BaseWindow protocol WM_DELETE_WINDOW registered for {self.__class__.__name__}"
        )

    def on_close(self):
        logging.info(f"BaseWindow.on_close called for {self.__class__.__name__}")
        try:
            pointer_x = self.winfo_pointerx()
            pointer_y = self.winfo_pointery()
            containing = self.winfo_containing(pointer_x, pointer_y)
            containing_name = containing.__class__.__name__ if containing else "None"
        except Exception:
            pointer_x = pointer_y = None
            containing_name = "unknown"

        focus_widget = self.focus_get()
        focus_name = focus_widget.__class__.__name__ if focus_widget else "None"

        logging.info(
            f"BaseWindow.on_close context: focus={focus_name}, "
            f"pointer=({pointer_x},{pointer_y}), containing={containing_name}, "
            f"viewable={self.winfo_viewable()}, "
            f"x={self.winfo_x()}, y={self.winfo_y()}"
        )
        logging.info("BaseWindow.on_close stack:\n" + "".join(traceback.format_stack()))
        self.destroy()
