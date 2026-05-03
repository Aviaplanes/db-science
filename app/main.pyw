import os
import sys
from pathlib import Path

# Ensure the UI package is importable
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from ui.window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.run()
