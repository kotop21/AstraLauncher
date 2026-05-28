from core.events import bus, Signal


class InstanceSelectorActions:
    def __init__(self, widget):
        self.widget = widget

    def start_server(self):
        if hasattr(self.widget, "_current_context_data"):
            bus.emit(
                Signal.CMD_START_SERVER,
                server_id=self.widget._current_context_data["id"],
            )

    def stop_server(self):
        if hasattr(self.widget, "_current_context_data"):
            bus.emit(
                Signal.CMD_STOP_SERVER,
                server_id=self.widget._current_context_data["id"],
            )

    def delete_server(self):
        if hasattr(self.widget, "_current_context_data"):
            bus.emit(
                Signal.CMD_DELETE_SERVER,
                server_id=self.widget._current_context_data["id"],
            )

    def open_folder(self):
        if hasattr(self.widget, "_current_context_data"):
            server_path = self.widget._current_context_data.get("path")
            if server_path:
                bus.emit(Signal.CMD_OPEN_FOLDER, path=server_path)

    def on_single_click(self, row_index, server_id):
        for i, frame in enumerate(self.widget.row_frames):
            frame.configure(
                fg_color=self.widget.selected_color
                if i == row_index
                else self.widget.default_color
            )
        bus.emit(Signal.CMD_REQUEST_SERVER, server_id=server_id)

    def on_double_click(self, data):
        self.widget._current_context_data = data
        self.widget.cmd_manage._on_click()
