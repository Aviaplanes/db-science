import json
import tkinter as tk

from constants.colors import theme
from constants.fonts import PAGE_TITLE
from constants.paths import EQUIPMENT_JSON
from constants.settings import NAV_ITEMS
from ui.dashboard_widgets import FilterBar, StatCard, fill_table, make_table


def load_equipment() -> list[dict]:
    if EQUIPMENT_JSON.is_file():
        with open(EQUIPMENT_JSON, encoding="utf-8") as f:
            return json.load(f)
    return []


class EquipmentPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=theme.bg)
        self.pack(fill="both", expand=True, padx=24, pady=20)
        self.data = load_equipment()
        self._build_header()
        self._build_filter()
        self._build_table()
        self._apply_filter("")

    def _build_header(self):
        title = next((label for key, label in NAV_ITEMS if key == "equipment"), "")
        
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
            ("Название", 220),
            ("Категория", 160),
            ("Серийный №", 140),
            ("Производитель", 140),
            ("Цена, ₽", 100),
            ("Поставщик ID", 100),
        ]
        self.table = make_table(self, columns)

    def _apply_filter(self, query: str):
        q = query.lower()
        rows = []
        for e in self.data:
            searchable = " ".join(str(v) for v in e.values()).lower()
            if q in searchable:
                rows.append(
                    (
                        e.get("equipment_id", ""),
                        e.get("name", ""),
                        e.get("category", ""),
                        e.get("serial_number", ""),
                        e.get("manufacturer", ""),
                        f"{e.get('price', 0):,.2f}",
                        e.get("supplier_id", ""),
                    )
                )
        fill_table(self.table, rows)
