import os
import shlex
import shutil
import subprocess
from pathlib import Path


def run_jar(
    jar_path: str, java_args: str, cwd: str, core_name: str = ""
) -> subprocess.Popen:
    java_exec = shutil.which("java")
    if not java_exec:
        print(
            f"[Core-util] Error: 'java' executable not found in PATH. Cannot start jar {jar_path}"
        )
        return None

    args = [java_exec] + shlex.split(java_args) + ["-jar", jar_path]

    no_gui_cores = ["velocity", "bungeecord", "waterfall"]

    jar_filename = Path(jar_path).name.lower()
    is_proxy = any(
        proxy in core_name.lower() or proxy in jar_filename for proxy in no_gui_cores
    )

    if not is_proxy:
        args.append("--nogui")

    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NO_WINDOW

    try:
        process = subprocess.Popen(
            args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            creationflags=creationflags,
        )
    except FileNotFoundError as e:
        print(f"[Core-util] Failed to start process: {e}")
        return None

    print(f"[Core-util] Run jar: {' '.join(args)}")
    return process
