from typing import Dict
from core.events import bus, Signal
from core.components import BaseListener, listen_to
from core.state import state


class AddServerListener(BaseListener):
    @listen_to(Signal.CMD_ADD_SERVER)
    def handle_add(self, server_data: Dict):
        print(f"[Core] Добавление нового сервера: {server_data.get('name')}...")

        new_id = state.add_server(server_data)

        updated_data = state.get_server(new_id)
        bus.emit(Signal.SERVER_ADDED, server_data=updated_data)
