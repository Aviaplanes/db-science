# Тёмная тема — мягкая, не кислотная
DARK = {
    "bg": "#090810",
    "sidebar_bg": "#161b27",
    "card_bg": "#1c2333",
    "card_border": "#2a3347",
    "accent": "#4f8ef7",
    "accent_hover": "#6aa3ff",
    "danger": "#e05c6a",
    "success": "#4caf82",
    "text": "#e2e8f0",
    "text_muted": "#64748b",
    "hover_bg": "#232d42",
    "table_row_odd": "#161b27",
    "table_row_even": "#1c2333",
    "table_select": "#2a3f6e",
    "table_heading_bg": "#1c2333",
    "input_bg": "#1c2333",
    "scrollbar": "#2a3347",
    "toggle_bg": "#2a3347",
}

# Светлая тема — чистая, не слепит
LIGHT = {
    "bg": "#f0f4f8",
    "sidebar_bg": "#ffffff",
    "card_bg": "#ffffff",
    "card_border": "#dde3ed",
    "accent": "#3b76ef",
    "accent_hover": "#2563d6",
    "danger": "#d94f5c",
    "success": "#34a371",
    "text": "#1a202c",
    "text_muted": "#718096",
    "hover_bg": "#eef2fc",
    "table_row_odd": "#f8fafc",
    "table_row_even": "#ffffff",
    "table_select": "#dbeafe",
    "table_heading_bg": "#f1f5f9",
    "input_bg": "#ffffff",
    "scrollbar": "#dde3ed",
    "toggle_bg": "#e2e8f0",
}


class ThemeColors:
    """Хранит текущую тему. Используется как синглтон — один объект на всё приложение."""

    def __init__(self):
        self._dark = True  # по умолчанию тёмная
        self._apply()

    def _apply(self):
        palette = DARK if self._dark else LIGHT
        for key, value in palette.items():
            setattr(self, key, value)

    def switch(self):
        """Переключить тему и применить новые атрибуты."""
        self._dark = not self._dark
        self._apply()

    @property
    def is_dark(self) -> bool:
        return self._dark


# Единственный экземпляр — импортируется везде
theme = ThemeColors()
