import customtkinter as ctk
from app.config import CONFIG
from app.views import MainView, FailedView
from app.services import start_socket_client,stop_socket_client

class App:
    def __init__(self):
        self.root = ctk.CTk()
        start_socket_client()
        self._configure_window()
        self._build_layout()
        self._show_main()
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_window(self):
        self.root.title(CONFIG.APP_TITLE)
        self.root.geometry(f"{CONFIG.WINDOW_WIDTH}x{CONFIG.WINDOW_HEIGHT}")
        self.root.minsize(CONFIG.WINDOW_MIN_WIDTH, CONFIG.WINDOW_MIN_HEIGHT)

    def _build_layout(self):
        header = ctk.CTkFrame(self.root)
        header.pack(fill="x", padx=10, pady=8)

        ctk.CTkButton(
            header,
            text="Tickets activos",
            command=self._show_main
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            header,
            text="Tickets fallidos",
            command=self._show_failed
        ).pack(side="left")

        self.view_container =  ctk.CTkFrame(self.root)
        self.view_container.pack(fill="both", expand=True)

        self.main_view = MainView(self.view_container)
        self.failed_view = FailedView(self.view_container)

    def _show_main(self):
        self.failed_view.pack_forget()
        self.main_view.pack(fill="both", expand=True)

    def _show_failed(self):
        self.main_view.pack_forget()
        self.failed_view.pack(fill="both", expand=True)

    def _on_close(self):
        stop_socket_client()
        self.root.destroy()

    def run(self):
        self.root.mainloop()