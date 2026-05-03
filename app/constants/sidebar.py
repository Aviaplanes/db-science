# Цвета sidebar
SIDEBAR_BG = "#090810"
SIDEBAR_TEXT = "#727079"
SIDEBAR_ACTIVE_TEXT = "white"
SIDEBAR_BORDER = "#1a1720"

# Заголовки секций
SIDEBAR_DASHBOARD = "Dashboard"
SIDEBAR_DATABASE = "Database"

# Настройки кнопок
BUTTON_HEIGHT = 44
BUTTON_PADX = 8
BUTTON_PADY = 1
GRADIENT_START = "#2C1F5B"
GRADIENT_END = "#0A0911"

# Размеры
HEADER_FONT_SIZE = 9
HEADER_PADY = 12
HEADER_PADX = 16

# Границы
BORDER_WIDTH = 4


def get_page_titles(nav_items):
    """Генерирует PAGE_TITLES из NAV_ITEMS (с эмодзи)"""
    return {key: label for key, label in nav_items}


def get_default_page(nav_items):
    """Возвращает первую страницу из списка"""
    return nav_items[0][0] if nav_items else "overview"


def get_button_by_key(nav_items, key):
    """Возвращает название кнопки по ключу"""
    for k, label in nav_items:
        if k == key:
            return label
    return ""


def get_greeting(user_name, morning_start=6, day_start=12, evening_start=18, night_start=22):
    """
    Возвращает приветствие в зависимости от времени суток (английский)
    morning: 6-11 (Morning)
    day: 12-17 (Afternoon)
    evening: 18-21 (Evening)
    night: 22-5 (Night)
    """
    from datetime import datetime
    
    hour = datetime.now().hour
    
    if morning_start <= hour < day_start:
        greeting = "Morning"
    elif day_start <= hour < evening_start:
        greeting = "Afternoon"
    elif evening_start <= hour < night_start:
        greeting = "Evening"
    else:
        greeting = "Night"
    
    return f"{greeting} {user_name}"