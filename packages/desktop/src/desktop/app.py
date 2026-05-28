from desktop.windows import MainWindow
import customtkinter as ctk
import core.listeners
from core import BaseStorage


def main():
    _bs = BaseStorage()
    app = MainWindow()
    print("Starting desktop launcher!")
    app.mainloop()


if __name__ == "__main__":
    main()
