import tkinter as tk

from constants.colors import theme
from constants.fonts import PAGE_TITLE
from constants.settings import NAV_ITEMS


class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=theme.bg)
        self.pack(fill="both", expand=True, padx=24, pady=20)
        self._build_header()

def _build_header(self):
        title = next((label for key, label in NAV_ITEMS if key == "settings"), "")
        
        tk.Label(
            self,
            text=title,
            font=PAGE_TITLE,
            bg=theme.bg,
            fg=theme.text,
            anchor="w",
        ).pack(fill="x", pady=(0, 16))

        tk.Label(
            self,
            text="Здесь будут настройки приложения...",
            font=("Segoe UI", 12),
            bg=theme.bg,
            fg=theme.text_muted,
            anchor="w",
        ).pack(fill="x", pady=(20, 0))
