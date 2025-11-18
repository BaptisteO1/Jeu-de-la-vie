 
import sys
import logging
from PyQt6.QtWidgets import QApplication
from core.config import Config
from gui.main_window import MainWindow

def main():
    # Récupérer l'argument de ligne de commande pour le mode debug
    debug = "--debug" in sys.argv
    Config.set_debug(debug)
    Config.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Lancement en mode {'DEBUG' if debug else 'RELEASE'}")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
