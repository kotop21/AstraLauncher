from typing import Dict, List, Optional
from core import InstanceStorage


class CoreState(InstanceStorage):
    def __init__(self):
        super().__init__()
        self.filename = "instance.json"
        self.servers: Dict[int, Dict] = self._load_data()

    def _load_data(self) -> Dict[int, Dict]:
        raw_data = self.load_json(self.filename, default={})
        parsed_data = {}
        for k, v in raw_data.items():
            server_id = int(k)
            v["status"] = "Stopped"
            v["process_key"] = None
            if "path" not in v:
                v["path"] = ""
            if "java_args" not in v:
                v["java_args"] = "-Xmx4G -Xms1G"
            parsed_data[server_id] = v
        return parsed_data

    def save(self):
        data_to_save = {}
        for k, v in self.servers.items():
            save_copy = v.copy()
            save_copy.pop("status", None)
            save_copy.pop("process_key", None)
            data_to_save[k] = save_copy
        self.save_json(self.filename, data_to_save)

    def get_all(self) -> List[Dict]:
        return list(self.servers.values())

    def get_server(self, server_id: int) -> Optional[Dict]:
        return self.servers.get(server_id)

    def add_server(self, server_data: Dict) -> int:
        new_id = max(self.servers.keys(), default=0) + 1
        server_data["id"] = new_id
        server_data["status"] = "Stopped"
        server_data["process_key"] = None
        server_data["path"] = self.create_instance_folder(new_id, server_data["name"])

        if "java_args" not in server_data:
            server_data["java_args"] = "-Xmx4G -Xms1G"

        self.servers[new_id] = server_data
        self.save()
        return new_id

    def update_server_status(self, server_id: int, new_status: str, process_key=None):
        if server_id in self.servers:
            self.servers[server_id]["status"] = new_status
            if process_key is not None:
                self.servers[server_id]["process_key"] = process_key

    def update_server_java_args(self, server_id: int, java_args: str):
        if server_id in self.servers:
            self.servers[server_id]["java_args"] = java_args
            self.save()

    def delete_server(self, server_id: int):
        if server_id in self.servers:
            path = self.servers[server_id].get("path")
            if path:
                self.delete_instance_folder(path)
            del self.servers[server_id]
            self.save()


state = CoreState()
