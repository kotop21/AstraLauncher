from core.events import Signal
from core.components import BaseListener, listen_to


class TestListener(BaseListener):
    @listen_to(Signal.TEST_SIGNAL)
    def handle_test(self, data: str):
        print(f"[Logger] Получен тестовый сигнал: {data}")
