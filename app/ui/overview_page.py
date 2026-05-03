import tkinter as tk

from constants.colors import theme
from constants.fonts import PAGE_TITLE
from constants.settings import NAV_ITEMS


class OverviewPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=theme.bg)
        self.pack(fill="both", expand=True, padx=24, pady=20)
        self._build_header()

    def _build_header(self):
        title = next((label for key, label in NAV_ITEMS if key == "overview"), "")
        
        tk.Label(
            self,
            text=title,
            font=PAGE_TITLE,
            bg=theme.bg,
            fg=theme.text,
            anchor="w",
        ).pack(fill="x", pady=(0, 16))