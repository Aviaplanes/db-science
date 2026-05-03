import tkinter as tk

from constants.colors import theme
from constants.fonts import LOGO, NAV
from constants.paths import ICON
from constants.settings import (
    APP_GEOMETRY,
    APP_LOGO_TEXT,
    APP_MIN_SIZE,
    APP_TITLE,
    NAV_ITEMS,
    SIDEBAR_WIDTH,
    CARD_CORNER_RADIUS,
)
from constants.sidebar import (
    SIDEBAR_BG,
    SIDEBAR_TEXT,
    SIDEBAR_ACTIVE_TEXT,
    SIDEBAR_BORDER,
    SIDEBAR_DASHBOARD,
    SIDEBAR_DATABASE,
    BUTTON_HEIGHT,
    BUTTON_PADX,
    BUTTON_PADY,
    GRADIENT_START,
    GRADIENT_END,
    HEADER_FONT_SIZE,
    HEADER_PADY,
    HEADER_PADX,
    BORDER_WIDTH,
    get_page_titles,
    get_default_page,
    get_button_by_key,
)
from ui.dashboard_widgets import _draw_rounded_rect
from PIL import Image, ImageDraw, ImageTk


# Генерируем константы из NAV_ITEMS
PAGE_TITLES = get_page_titles(NAV_ITEMS)
DEFAULT_PAGE = get_default_page(NAV_ITEMS)


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(APP_GEOMETRY)
        self.root.minsize(*APP_MIN_SIZE)
        self.root.configure(bg=theme.bg)

        # Загрузка кастомных шрифтов
        self._load_custom_fonts()

        self._set_icon()
        self._build_layout()
        self._show_page("overview")

    def _load_custom_fonts(self):
        """Загружает кастомные шрифты Syne"""
        from tkinter import font as tkfont
        import os
        
        fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts", "Syne")
        
        # Создаём именованные шрифты из файлов
        font_configs = [
            ("SyneRegular", "Syne-Regular.ttf", "normal"),
            ("SyneBold", "Syne-Bold.ttf", "bold"),
            ("SyneSemiBold", "Syne-SemiBold.ttf", "normal"),
            ("SyneExtraBold", "Syne-ExtraBold.ttf", "bold"),
            ("SyneMedium", "Syne-Medium.ttf", "normal"),
        ]
        
        for font_name, filename, weight in font_configs:
            font_path = os.path.join(fonts_dir, filename)
            if os.path.exists(font_path):
                try:
                    # Создаём шрифт с уникальным именем
                    f = tkfont.Font(file=font_path, name=font_name, exists=True)
                except:
                    pass

    def _set_icon(self):
        if ICON.is_file():
            try:
                self.root.iconbitmap(str(ICON))
            except Exception:
                pass

    def _build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=SIDEBAR_WIDTH)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Толстая граница между панелью и правой частью
        border_frame = tk.Frame(self.root, bg=SIDEBAR_BORDER, width=BORDER_WIDTH)
        border_frame.pack(side="left", fill="y")

        # Основная часть (справа)
        self.content = tk.Frame(self.root, bg=SIDEBAR_BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Верхняя панель с названием вкладки
        self.content_header = tk.Frame(self.content, bg=SIDEBAR_BG, height=48)
        self.content_header.pack(fill="x")
        self.content_header.pack_propagate(False)

        # Метка для названия страницы (будет обновляться при смене страницы)
        self.page_title_label = tk.Label(
            self.content_header,
            text="",
            font=NAV,
            bg=SIDEBAR_BG,
            fg=SIDEBAR_ACTIVE_TEXT,
            anchor="w",
            padx=HEADER_PADX,
        )
        self.page_title_label.pack(fill="x", pady=HEADER_PADY)

        # Граница снизу верхней панели (как у левой панели)
        header_border = tk.Frame(self.content, bg=SIDEBAR_BORDER, height=BORDER_WIDTH)
        header_border.pack(fill="x")

        # Фрейм для контента страницы
        self.content_body = tk.Frame(self.content, bg=SIDEBAR_BG)
        self.content_body.pack(fill="both", expand=True)

        self._build_sidebar()

    def _build_sidebar(self):
        # Очистка сайдбара для перерисовки при смене темы
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        self.sidebar.configure(bg=SIDEBAR_BG)

        # Заголовок сайдбара (как Database)
        header_label = tk.Label(
            self.sidebar,
            text=SIDEBAR_DASHBOARD,
            font=("Segoe UI", HEADER_FONT_SIZE),
            bg=SIDEBAR_BG,
            fg=SIDEBAR_TEXT,
            anchor="w",
            padx=HEADER_PADX,
            pady=HEADER_PADY,
        )
        header_label.pack(fill="x")

        # Фрейм для кнопок навигации (Overview)
        nav_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        nav_frame.pack(fill="x")

        self.nav_buttons = {}
        # Только Overview в основной навигации
        overview_item = [item for item in NAV_ITEMS if item[0] == "overview"][0]
        self.nav_buttons["overview"] = self._nav_button(overview_item[1], "overview", nav_frame)

        # Секция Database - отдельный фрейм
        db_section = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        db_section.pack(fill="x")

        db_header = tk.Label(
            db_section,
            text=SIDEBAR_DATABASE,
            font=("Segoe UI", HEADER_FONT_SIZE),
            bg=SIDEBAR_BG,
            fg=SIDEBAR_TEXT,
            anchor="w",
            padx=HEADER_PADX,
            pady=HEADER_PADY,
        )
        db_header.pack(fill="x")

        # Кнопки базы данных (все кроме overview и settings)
        db_buttons_frame = tk.Frame(db_section, bg=SIDEBAR_BG)
        db_buttons_frame.pack(fill="x")

        for page_name, label in NAV_ITEMS:
            if page_name not in ("overview", "settings"):
                self.nav_buttons[page_name] = self._nav_button(label, page_name, db_buttons_frame)

        # Кнопка Настройки в самом низу
        bottom_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        bottom_frame.pack(side="bottom", fill="x", pady=(0, 8))
        self.nav_buttons["settings"] = self._nav_button(get_button_by_key(NAV_ITEMS, "settings"), "settings", bottom_frame)

    def _nav_button(self, label: str, page_name: str, parent=None) -> tk.Label:
        # Кнопка навигации с градиентным фоном
        if parent is None:
            parent = self.sidebar

        is_active = self._active_page == page_name
        active_text_color = SIDEBAR_ACTIVE_TEXT
        inactive_text_color = SIDEBAR_TEXT
        text_color = active_text_color if is_active else inactive_text_color

        btn_canvas = tk.Canvas(
            parent,
            height=BUTTON_HEIGHT,
            bg=theme.bg,
            highlightthickness=0,
            cursor="hand2",
        )
        btn_canvas.pack(fill="x", pady=BUTTON_PADY, padx=BUTTON_PADX)

        def _draw_btn():
            btn_canvas.delete("all")
            w = btn_canvas.winfo_width()
            h = btn_canvas.winfo_height()
            if w > 0 and h > 0:
                if is_active:
                    # Gradient background for active button
                    start_rgb = tuple(int(GRADIENT_START[i:i+2], 16) for i in (1, 3, 5))
                    end_rgb = tuple(int(GRADIENT_END[i:i+2], 16) for i in (1, 3, 5))
                    img = Image.new("RGBA", (w, h))
                    for x in range(w):
                        ratio = x / (w - 1) if w > 1 else 0
                        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
                        img.paste((r, g, b, 255), (x, 0, x + 1, h))
                    # Rounded mask
                    mask = Image.new("L", (w, h), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.rounded_rectangle((0, 0, w, h), radius=CARD_CORNER_RADIUS, fill=255)
                    img.putalpha(mask)
                    photo = ImageTk.PhotoImage(img)
                    btn_canvas.create_image(0, 0, anchor="nw", image=photo)
                    btn_canvas._img = photo
                else:
                    # Solid background for inactive button (match sidebar color)
                    _draw_rounded_rect(
                        btn_canvas,
                        0,
                        0,
                        w,
                        h,
                        CARD_CORNER_RADIUS,
                        fill=SIDEBAR_BG,
                        outline="",
                    )
                # Button text
                btn_canvas.create_text(
                    24,
                    h // 2,
                    text=label,
                    anchor="w",
                    font=NAV,
                    fill=text_color,
                )

        # Initial draw and update on resize
        btn_canvas.bind("<Configure>", lambda e: _draw_btn())
        # Hover does not change appearance
        btn_canvas.bind("<Enter>", lambda e: _draw_btn())
        btn_canvas.bind("<Leave>", lambda e: _draw_btn())
        # Click handler
        btn_canvas.bind("<Button-1>", lambda e: self._show_page(page_name) if page_name != self._active_page else None)

        return btn_canvas

    # ── Переключение страниц ──────────────────────────────────────────────
    _active_page: str = ""

    def _show_page(self, page_name: str):
        self._active_page = page_name
        self._build_sidebar()  # Обновляем подсветку кнопок

        # Обновляем заголовок в верхней панели
        self.page_title_label.configure(text=PAGE_TITLES.get(page_name, ""))

        # Очищаем контент
        for widget in self.content_body.winfo_children():
            widget.destroy()

        self.content_body.configure(bg=SIDEBAR_BG)

        if page_name == "overview":
            from ui.overview_page import OverviewPage

            OverviewPage(self.content_body)
        elif page_name == "equipment":
            from ui.equipment_page import EquipmentPage

            EquipmentPage(self.content_body)
        elif page_name == "people":
            from ui.people_page import PeoplePage

            PeoplePage(self.content_body)
        elif page_name == "transactions":
            from ui.transactions_page import TransactionsPage

            TransactionsPage(self.content_body)
        elif page_name == "settings":
            from ui.settings_page import SettingsPage

            SettingsPage(self.content_body)

    def run(self):
        self.root.mainloop()
