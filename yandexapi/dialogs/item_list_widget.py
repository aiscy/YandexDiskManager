from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from yandexapi.ui.item_widget_ui import Ui_Form


class ItemListWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    @pyqtSlot(str)
    def setPixmap(self, ext):
        if ext == '.zip':
            self.label.setPixmap(QPixmap(':/fileicon/zip.png'))
        elif ext == '.rar':
            self.label.setPixmap(QPixmap(':/fileicon/rar.png'))
        elif ext == '.7z':
            self.label.setPixmap(QPixmap(':/fileicon/7zip.png'))
        else:
            self.label.setPixmap(QPixmap(':/fileicon/file.png'))

    @pyqtSlot(str)
    def setName(self, name):
        self.label_name.setText(name)

    @pyqtSlot(str)
    def setInfo(self, info):
        self.label_info.setText(info)

    @pyqtSlot(float)
    def setProgress(self, value):
        self.progressBar.setValue(value)

    @pyqtSlot()
    def hideProgress(self):
        self.progressBar.hide()