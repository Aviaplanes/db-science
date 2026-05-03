import tkinter as tk
from tkinter import ttk

from constants.colors import theme
from constants.fonts import (
    SEARCH,
    STAT_ICON,
    STAT_LABEL,
    STAT_VALUE,
    TABLE_HEADING,
    TABLE_ROW,
)
from constants.settings import CARD_CORNER_RADIUS


# ── Хелпер для скругленных прямоугольников ────────────────────────────────
def _draw_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r,
        y1,
        x1 + r,
        y1,
        x2 - r,
        y1,
        x2 - r,
        y1,
        x2,
        y1,
        x2,
        y1 + r,
        x2,
        y1 + r,
        x2,
        y2 - r,
        x2,
        y2 - r,
        x2,
        y2,
        x2 - r,
        y2,
        x2 - r,
        y2,
        x1 + r,
        y2,
        x1 + r,
        y2,
        x1,
        y2,
        x1,
        y2 - r,
        x1,
        y2 - r,
        x1,
        y1 + r,
        x1,
        y1 + r,
        x1,
        y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ── Карточка статистики ──────────────────────────────────────────────────────
class StatCard(tk.Canvas):
    """Иконка + число + подпись с эффектом скругления и легкой тени."""

    def __init__(self, parent, icon: str, value: str, label: str, **kwargs):
        super().__init__(
            parent, height=110, bg=theme.bg, highlightthickness=0, **kwargs
        )
        # Сохраняем данные для отрисовки
        self._icon = icon
        self._value = value
        self._label = label
        # Перерисовываем при изменении размеров
        self.bind("<Configure>", self._draw)
        # Первичная отрисовка
        self._draw()

    def _draw(self, event=None):
        # Очистка предыдущего рисунка
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        r = CARD_CORNER_RADIUS
        # Тень
        _draw_rounded_rect(
            self,
            4,
            4,
            w - 4,
            h - 4,
            r,
            fill=theme.card_border,
            outline="",
        )
        # Основная карточка
        _draw_rounded_rect(
            self,
            2,
            2,
            w - 6,
            h - 6,
            r,
            fill=theme.card_bg,
            outline="",
        )
        # Текст, центрированный по ширине
        self.create_text(w // 2, int(h * 0.255), text=self._icon, font=STAT_ICON, fill=theme.accent)
        self.create_text(w // 2, int(h * 0.53), text=self._value, font=STAT_VALUE, fill=theme.text)
        self.create_text(w // 2, int(h * 0.78), text=self._label, font=STAT_LABEL, fill=theme.text_muted)


# ── Строка поиска ────────────────────────────────────────────────────────────
class FilterBar(tk.Canvas):
    """Поле поиска с плейсхолдером и скругленным фоном."""

    def __init__(self, parent, on_search=None, **kwargs):
        super().__init__(parent, height=50, bg=theme.bg, highlightthickness=0, **kwargs)
        self._on_search = on_search
        self._var = tk.StringVar()
        self._var.trace_add("write", self._fire)

        # Скругленный фон инпута
        _draw_rounded_rect(
            self, 0, 4, 400, 46, 12, fill=theme.card_bg, outline=theme.card_border
        )

        # Иконка поиска
        self.create_text(24, 25, text="🔍", font=SEARCH, fill=theme.text_muted)

        # Накладываем прозрачный Entry поверх Canvas
        self._entry = tk.Entry(
            self,
            textvariable=self._var,
            font=SEARCH,
            bg=theme.card_bg,
            fg=theme.text,
            insertbackground=theme.text,
            relief="flat",
            width=28,
            borderwidth=0,
            highlightthickness=0,
        )
        self.create_window(56, 25, window=self._entry, anchor="w")

        self._entry.insert(0, "Поиск...")
        self._entry.bind("<FocusIn>", self._clear_placeholder)
        self._entry.bind("<FocusOut>", self._set_placeholder)

    def _clear_placeholder(self, _event):
        if self._entry.get() == "Поиск...":
            self._entry.delete(0, "end")
            self._entry.configure(fg=theme.text)

    def _set_placeholder(self, _event):
        if not self._entry.get():
            self._entry.insert(0, "Поиск...")
            self._entry.configure(fg=theme.text_muted)

    def _fire(self, *_):
        val = self._var.get()
        if val != "Поиск..." and self._on_search:
            self._on_search(val)

    def get(self) -> str:
        val = self._var.get()
        return "" if val == "Поиск..." else val


# ── Таблица ──────────────────────────────────────────────────────────────────
def make_table(parent, columns: list[tuple[str, int]]) -> ttk.Treeview:
    style = ttk.Style()
    style.theme_use("clam")

    # Современные стили для таблицы
    style.configure(
        "Modern.Treeview",
        background=theme.table_row_odd,
        foreground=theme.text,
        fieldbackground=theme.table_row_odd,
        rowheight=32,
        font=TABLE_ROW,
        borderwidth=0,
    )
    style.configure(
        "Modern.Treeview.Heading",
        background=theme.table_heading_bg,
        foreground=theme.accent,
        font=TABLE_HEADING,
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Modern.Treeview",
        background=[("selected", theme.table_select)],
        foreground=[("selected", "white")],
    )

    col_ids = [c[0] for c in columns]

    # Canvas с закруглённым фоном вокруг таблицы
    outer_canvas = tk.Canvas(parent, bg=theme.bg, highlightthickness=0)
    outer_canvas.pack(fill="both", expand=True, pady=(8, 0))

    def _draw_bg(event=None):
        outer_canvas.delete("bg_rect")
        w = outer_canvas.winfo_width()
        h = outer_canvas.winfo_height()
        if w > 0 and h > 0:
            _draw_rounded_rect(
                outer_canvas,
                4,
                4,
                w - 4,
                h - 4,
                CARD_CORNER_RADIUS,
                fill=theme.card_bg,
                outline=theme.card_border,
                tags="bg_rect",
            )
            # Обновляем размер окна с внутренним Frame
            outer_canvas.coords(inner_window, 4, 4)
            outer_canvas.itemconfig(inner_window, width=w - 8, height=h - 8)

    outer_canvas.bind("<Configure>", _draw_bg)

    # Внутренний Frame для Treeview и Scrollbar
    inner_frame = tk.Frame(outer_canvas, bg=theme.bg)
    inner_window = outer_canvas.create_window(0, 0, anchor="nw", window=inner_frame)

    tree = ttk.Treeview(
        inner_frame,
        columns=col_ids,
        show="headings",
        style="Modern.Treeview",
        selectmode="browse",
    )
    for col_id, width in columns:
        tree.heading(col_id, text=col_id)
        tree.column(col_id, width=width, anchor="w", minwidth=60)

    tree.tag_configure("odd", background=theme.table_row_odd)
    tree.tag_configure("even", background=theme.table_row_even)

    scrollbar = ttk.Scrollbar(inner_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return tree


def fill_table(tree: ttk.Treeview, rows: list[tuple]):
    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        tag = "even" if i % 2 == 0 else "odd"
        tree.insert("", "end", values=row, tags=(tag,))
