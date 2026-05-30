from .base_api import BaseAPI


class PurpurAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.purpurmc.org/v2"

    def get_versions(self, project: str) -> list:
        url = f"{self.base_url}/{project}"
        data = self.fetch_json(url)
        return data.get("versions", [])[::-1]

    def get_builds(self, project: str, version: str) -> list:
        url = f"{self.base_url}/{project}/{version}"
        data = self.fetch_json(url)
        builds = data.get("builds", {}).get("all", [])
        return builds[::-1]

    def get_download_url(self, project: str, version: str, build: str) -> str:
        return f"{self.base_url}/{project}/{version}/{build}/download"
