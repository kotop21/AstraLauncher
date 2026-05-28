from enum import Enum, auto
from typing import Callable, Dict, List


class Signal(Enum):
    CMD_ADD_SERVER = auto()
    CMD_DELETE_SERVER = auto()
    CMD_START_SERVER = auto()
    CMD_STOP_SERVER = auto()
    CMD_KILL_SERVER = auto()
    CMD_REQUEST_ALL_SERVERS = auto()
    CMD_REQUEST_SERVER = auto()
    CMD_UPDATE_JAVA_ARGS = auto()
    CMD_OPEN_FOLDER = auto()

    SERVER_ADDED = auto()
    SERVER_DELETED = auto()
    SERVER_STATUS_CHANGED = auto()
    RESPONSE_ALL_SERVERS = auto()
    RESPONSE_SERVER = auto()

    TEST_SIGNAL = auto()


class StrictEventBus:
    def __init__(self):
        self._listeners: Dict[Signal, List[Callable]] = {sig: [] for sig in Signal}

    def subscribe(self, signal: Signal, callback: Callable):
        if not callable(callback):
            raise TypeError("Callback должен быть вызываемой функцией/методом.")
        self._listeners[signal].append(callback)

    def unsubscribe(self, signal: Signal, callback: Callable):
        if callback in self._listeners[signal]:
            self._listeners[signal].remove(callback)

    def emit(self, signal: Signal, **kwargs):
        if not self._listeners[signal]:
            raise RuntimeError(
                f"[EventBus] Ошибка безопасности: Сигнал {signal.name} отправлен, "
                "но на него никто не подписан!"
            )

        for callback in self._listeners[signal]:
            callback(**kwargs)


bus = StrictEventBus()
