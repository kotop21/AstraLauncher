from core.events import bus, Signal
from core.components import BaseListener, listen_to
from core.state import state


class StartServerListener(BaseListener):
    @listen_to(Signal.CMD_START_SERVER)
    def handle_start(self, server_id: int):
        state.update_server_status(server_id, "Running")
        bus.emit(
            Signal.SERVER_STATUS_CHANGED, server_id=server_id, new_status="Running"
        )
