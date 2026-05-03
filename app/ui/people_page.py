import json
import tkinter as tk

from constants.colors import theme
from constants.fonts import PAGE_TITLE
from constants.paths import PEOPLE_JSON
from constants.settings import NAV_ITEMS
from ui.dashboard_widgets import FilterBar, StatCard, fill_table, make_table


def load_people() -> list[dict]:
    if PEOPLE_JSON.is_file():
        with open(PEOPLE_JSON, encoding="utf-8") as f:
            return json.load(f)
    return []


class PeoplePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=theme.bg)
        self.pack(fill="both", expand=True, padx=24, pady=20)
        self.data = load_people()
        self._build_header()
        self._build_filter()
        self._build_table()
        self._apply_filter("")

    def _build_header(self):
        title = next((label for key, label in NAV_ITEMS if key == "people"), "")
        
        tk.Label(
            self,
            text=title,
            font=PAGE_TITLE,
            bg=theme.bg,
            fg=theme.text,
            anchor="w",
        ).pack(fill="x", pady=(0, 16))

    def _build_filter(self):
        FilterBar(self, on_search=self._apply_filter).pack(fill="x", pady=(0, 4))

    def _build_table(self):
        columns = [
            ("ID", 50),
            ("Имя", 220),
            ("Телефон", 160),
            ("Email", 220),
            ("Роль", 120),
        ]
        self.table = make_table(self, columns)

    def _apply_filter(self, query: str):
        q = query.lower()
        rows = []
        for p in self.data:
            searchable = " ".join(str(v) for v in p.values()).lower()
            if q in searchable:
                rows.append(
                    (
                        p.get("person_id", ""),
                        p.get("full_name", ""),
                        p.get("phone", ""),
                        p.get("email", ""),
                        p.get("role", ""),
                    )
                )
        fill_table(self.table, rows)
