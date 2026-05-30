from core.base_storage import BaseStorage


class AppConfig(BaseStorage):
    def __init__(self):
        super().__init__()
        self.filename = "config.json"
        self.data = self.load_json(self.filename, default={})

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value):
        self.data[key] = value
        self.save_json(self.filename, self.data)


config = AppConfig()
