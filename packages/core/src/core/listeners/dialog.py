from core.events import bus, Signal
from core.components import BaseListener, listen_to
from core.utils.dialog_manager import DialogManager


class DialogListener(BaseListener):
    @listen_to(Signal.CMD_OPEN_DIR_DIALOG)
    def handle_open_dir(self, title: str = "Select Directory"):
        path = DialogManager.ask_directory(title=title)
        bus.emit(Signal.RESPONSE_DIR_DIALOG, path=path)
