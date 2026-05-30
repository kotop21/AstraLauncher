import tkinter.messagebox as messagebox
import customtkinter as ctk
from typing import List
from desktop.components import BaseWindow
from core.events import bus, Signal


class AddServerWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, title="Add Server", size=(400, 350))

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=40, pady=40)

        self.entry_name = ctk.CTkEntry(self.container, placeholder_text="Server Name")
        self.entry_name.pack(fill="x", pady=10)

        self.option_core = ctk.CTkOptionMenu(
            self.container,
            values=["Paper", "Purpur", "Import Local"],
            command=self._on_core_selected,
        )
        self.option_core.pack(fill="x", pady=10)

        self.option_version = ctk.CTkOptionMenu(
            self.container,
            values=["Select Core First..."],
            state="disabled",
            command=self._on_version_selected,
        )
        self.option_version.pack(fill="x", pady=10)

        self.option_build = ctk.CTkOptionMenu(
            self.container, values=["Select Version First..."], state="disabled"
        )
        self.option_build.pack(fill="x", pady=10)

        self.btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.btn_frame.pack(fill="x", pady=(20, 0))

        self.btn_cancel = ctk.CTkButton(
            self.btn_frame,
            text="Cancel",
            fg_color="transparent",
            border_width=1,
            command=self.destroy,
        )
        self.btn_cancel.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_confirm = ctk.CTkButton(
            self.btn_frame, text="Confirm", command=self._on_confirm
        )
        self.btn_confirm.pack(side="left", fill="x", expand=True, padx=(5, 0))

        bus.subscribe(Signal.RESPONSE_MC_VERSIONS, self._on_versions_received)
        bus.subscribe(Signal.RESPONSE_BUILD_VERSIONS, self._on_builds_received)
        bus.subscribe(Signal.RESPONSE_DIR_DIALOG, self._on_dir_selected)
        bus.subscribe(Signal.RESPONSE_SERVER_SCANNED, self._on_scanned)

        self.bind("<Destroy>", self._cleanup)

        self._on_core_selected(self.option_core.get())

    def _cleanup(self, event):
        if str(event.widget) == str(self):
            try:
                bus.unsubscribe(Signal.RESPONSE_MC_VERSIONS, self._on_versions_received)
                bus.unsubscribe(
                    Signal.RESPONSE_BUILD_VERSIONS, self._on_builds_received
                )
                bus.unsubscribe(Signal.RESPONSE_DIR_DIALOG, self._on_dir_selected)
                bus.unsubscribe(Signal.RESPONSE_SERVER_SCANNED, self._on_scanned)
            except ValueError:
                pass

    def _on_core_selected(self, core_name: str):
        if core_name == "Import Local":
            self.option_version.configure(state="disabled", values=["N/A (Import)"])
            self.option_version.set("N/A (Import)")
            self.option_build.configure(state="disabled", values=["N/A (Import)"])
            self.option_build.set("N/A (Import)")
            self.btn_confirm.configure(text="Select Folder")
            return

        self.btn_confirm.configure(text="Confirm")
        self.option_version.configure(state="disabled", values=["Loading..."])
        self.option_version.set("Loading...")
        self.option_build.configure(state="disabled", values=["Waiting..."])
        self.option_build.set("Waiting...")

        bus.emit(Signal.CMD_FETCH_MC_VERSIONS, core_name=core_name)

    def _on_versions_received(self, core_name: str, versions: List[str]):
        if self.option_core.get() == core_name:
            self.option_version.configure(state="normal", values=versions)
            if versions:
                self.option_version.set(versions[0])
                self._on_version_selected(versions[0])

    def _on_version_selected(self, mc_version: str):
        if self.option_core.get() == "Import Local":
            return

        self.option_build.configure(state="disabled", values=["Loading..."])
        self.option_build.set("Loading...")
        core_name = self.option_core.get()

        bus.emit(
            Signal.CMD_FETCH_BUILD_VERSIONS, core_name=core_name, mc_version=mc_version
        )

    def _on_builds_received(self, core_name: str, mc_version: str, builds: List[str]):
        if (
            self.option_core.get() == core_name
            and self.option_version.get() == mc_version
        ):
            self.option_build.configure(state="normal", values=builds)
            if builds:
                self.option_build.set(builds[0])

    def _on_confirm(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Server Name is required!")
            return

        core = self.option_core.get()
        if core == "Import Local":
            bus.emit(Signal.CMD_OPEN_DIR_DIALOG, title="Select Server Folder")
            return

        version = self.option_version.get()
        build = self.option_build.get()

        agree = messagebox.askyesno(
            "Minecraft EULA",
            "By installing this server, you must agree to the Minecraft EULA.\n\n"
            "Read it here: https://aka.ms/MinecraftEULA\n\n"
            "Do you agree to the EULA?",
        )

        if not agree:
            return

        server_data = {
            "name": name,
            "core": core,
            "version": version,
            "build": build,
            "port": 25565,
            "path": "",
        }

        bus.emit(Signal.CMD_ADD_SERVER, server_data=server_data)
        self.destroy()

    def _on_dir_selected(self, path: str):
        if not path:
            return
        bus.emit(Signal.CMD_SCAN_SERVER_DIR, path=path)

    def _on_scanned(self, server_data: dict):
        if server_data["core"] == "Unknown" and server_data["version"] == "Unknown":
            messagebox.showerror(
                "Invalid Directory",
                "This directory does not appear to be a valid Minecraft server.\nCould not find server .jar or configuration files.",
            )
            return

        custom_name = self.entry_name.get().strip()
        if custom_name:
            server_data["name"] = custom_name

        server_data["is_imported"] = True

        bus.emit(Signal.CMD_ADD_SERVER, server_data=server_data)
        self.destroy()
