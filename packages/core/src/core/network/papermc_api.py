from .base_api import BaseAPI


class PaperMCAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.papermc.io/v2/projects"

    def get_versions(self, project: str) -> list:
        url = f"{self.base_url}/{project}"
        data = self.fetch_json(url)
        return data.get("versions", [])[::-1]

    def get_builds(self, project: str, version: str) -> list:
        url = f"{self.base_url}/{project}/versions/{version}"
        data = self.fetch_json(url)
        builds = data.get("builds", [])
        return [str(b) for b in builds][::-1]

    def get_download_url(self, project: str, version: str, build: str) -> str:
        filename = f"{project}-{version}-{build}.jar"
        return f"{self.base_url}/{project}/versions/{version}/builds/{build}/downloads/{filename}"
