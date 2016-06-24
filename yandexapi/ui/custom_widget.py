from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QProgressBar


class CustomWidget(QWidget):
    def __init__ (self, parent = None):
        super(CustomWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel    = QLabel()
        self.textDownQLabel  = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        self.progressBar      = QProgressBar()
        self.allQHBoxLayout.addWidget(self.progressBar, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')
    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

