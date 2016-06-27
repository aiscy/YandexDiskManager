import logging
import sys

from PyQt5.QtWidgets import QApplication

from yandexapi.dialogs.main_ui import MainUI


if __name__ == '__main__':
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    app = QApplication(sys.argv)
    main_ui = MainUI()
    sys.exit(app.exec())
