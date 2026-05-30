import json
import urllib.request
from urllib.error import URLError


class BaseAPI:
    def fetch_json(self, url: str) -> dict:
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "ServLauncher/1.0"}
            )
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except URLError as e:
            print(f"[Network] Request failed for {url}: {e}")
            return {}

    def download_file(self, url: str, dest_path: str, progress_callback=None) -> bool:
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "ServLauncher/1.0"}
            )
            with (
                urllib.request.urlopen(req) as response,
                open(dest_path, "wb") as out_file,
            ):
                content_length = response.getheader("Content-Length")
                total_size = int(content_length) if content_length else 0
                downloaded = 0
                chunk_size = 8192

                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total_size)
            return True
        except Exception as e:
            print(f"[Network] Download failed for {url}: {e}")
            return False
