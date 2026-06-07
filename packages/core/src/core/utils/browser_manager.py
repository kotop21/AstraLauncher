import webbrowser


def open_url(url: str):
    print(f"[Core-util] Opening URL: {url}")
    webbrowser.open(url)
