from pathlib import Path

ROOT = Path(__file__).parents[2]
DB_DIR = ROOT / "db"
ASSETS_DIR = ROOT / "app" / "assets"
ICON = ASSETS_DIR / "icon.ico"

EQUIPMENT_JSON = DB_DIR / "equipment.json"
PEOPLE_JSON = DB_DIR / "people.json"
TRANSACTIONS_JSON = DB_DIR / "transactions.json"
