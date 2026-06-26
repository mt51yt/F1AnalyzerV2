from PySide6.QtWidgets import QApplication
from f1analyzer.ui.home import Home
from f1analyzer.config import CACHE_PATH
from fastf1 import Cache

if __name__ == "__main__":
    cache_dir: str = str( CACHE_PATH )
    Cache.enable_cache(cache_dir)

    app: QApplication = QApplication([])
    window: Home = Home()
    window.showMaximized()

    app.exec()