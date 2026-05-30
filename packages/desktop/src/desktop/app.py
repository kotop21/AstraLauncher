import tkinter.messagebox as messagebox
from desktop.windows import MainWindow
import core as core


def main():
    app = MainWindow()

    def on_closing():
        if messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit? All running servers will be stopped.",
        ):
            print("[Main] Initiating graceful shutdown for all servers...")
            core.bus.emit(core.Signal.CMD_SHUTDOWN_ALL)
            app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)

    print("Starting desktop launcher!")
    app.mainloop()


if __name__ == "__main__":
    main()
