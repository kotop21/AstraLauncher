from core.events import bus, Signal
from core.components import BaseListener, listen_to
from core.state import state


class StopServerListener(BaseListener):
    @listen_to(Signal.CMD_STOP_SERVER)
    def handle_stop(self, server_id: int):
        state.update_server_status(server_id, "Stopped")
        bus.emit(
            Signal.SERVER_STATUS_CHANGED, server_id=server_id, new_status="Stopped"
        )
