import json
import tkinter as tk

from constants.colors import theme
from constants.fonts import PAGE_TITLE
from constants.paths import TRANSACTIONS_JSON
from constants.settings import NAV_ITEMS
from ui.dashboard_widgets import FilterBar, StatCard, fill_table, make_table


def load_transactions() -> list[dict]:
    if TRANSACTIONS_JSON.is_file():
        with open(TRANSACTIONS_JSON, encoding="utf-8") as f:
            return json.load(f)
    return []


class TransactionsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=theme.bg)
        self.pack(fill="both", expand=True, padx=24, pady=20)
        self.data = load_transactions()
        self._build_header()
        self._build_filter()
        self._build_table()
        self._apply_filter("")

    def _build_header(self):
        title = next((label for key, label in NAV_ITEMS if key == "transactions"), "")
        
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
            ("Тип", 100),
            ("Оборудование ID", 120),
            ("Человек ID", 100),
            ("Кол-во", 80),
            ("Дата", 160),
            ("Заметка", 220),
        ]
        self.table = make_table(self, columns)

    def _apply_filter(self, query: str):
        q = query.lower()
        rows = []
        for t in self.data:
            searchable = " ".join(str(v) for v in t.values()).lower()
            if q in searchable:
                rows.append(
                    (
                        t.get("transaction_id", ""),
                        t.get("type", ""),
                        t.get("equipment_id", ""),
                        t.get("person_id", ""),
                        t.get("quantity", ""),
                        t.get("date", ""),
                        t.get("note", ""),
                    )
                )
        fill_table(self.table, rows)
