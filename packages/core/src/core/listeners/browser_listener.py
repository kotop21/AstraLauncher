from core.components import BaseListener, listen_to
from core.events import Signal
from core.utils import open_url


class BrowserListener(BaseListener):
    @listen_to(Signal.CMD_OPEN_URL)
    def handle_open_url(self, url: str):
        open_url(url)
