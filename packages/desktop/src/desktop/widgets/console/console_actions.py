from core.events import bus, Signal


class ConsoleActions:
    def __init__(self, widget):
        self.widget = widget

    def start_server(self):
        bus.emit(Signal.CMD_START_SERVER, server_id=self.widget.server_data["id"])

    def stop_server(self):
        bus.emit(Signal.CMD_STOP_SERVER, server_id=self.widget.server_data["id"])

    def kill_server(self):
        bus.emit(Signal.CMD_KILL_SERVER, server_id=self.widget.server_data["id"])

    def send_command(self, event=None):
        if self.widget.server_data["status"] != "Running":
            return

        command = self.widget.entry_cmd.get().strip()
        if command:
            # TODO: Emit command signal (e.g., bus.emit(Signal.CMD_SEND_CONSOLE, ...))
            print(
                f"[Console] Command sent to server {self.widget.server_data['id']}: {command}"
            )
            self.widget.entry_cmd.delete(0, "end")
