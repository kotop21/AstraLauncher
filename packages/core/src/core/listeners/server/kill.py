from core.events import bus, Signal
from core.components import BaseListener, listen_to
from core.state import state


class KillServerListener(BaseListener):
    @listen_to(Signal.CMD_KILL_SERVER)
    def handle_kill(self, server_id: int):
        state.update_server_status(server_id, "Stopped")
        bus.emit(
            Signal.SERVER_STATUS_CHANGED, server_id=server_id, new_status="Stopped"
        )
