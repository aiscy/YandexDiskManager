import os

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from yandexapi.ui.settings_ui import Ui_Dialog


class SettingsUI(QDialog, Ui_Dialog):
    settings_dict = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.toolButton.clicked.connect(lambda:self.lineEdit_watcher_folder.setText(QFileDialog.getExistingDirectory()))

    def isFirstRun(self):
        return self.settings.value('first_run', False)

    def getAPIKey(self):
        return self.settings.value('api_key')

    def getFolder(self):
        return self.settings.value('folder')

    # def getWhitelistExtensions(self):
    #     return self.settings.value('files_extension')

    def getMailServer(self):
        return self.settings.value('mail_server')

    def getMailError(self):
        return self.settings.value('mail_error')

    def accept(self):
        if not self.lineEdit_API.text():
            QMessageBox.critical(self, 'Ошибка', 'Укажите API ключ для доступа к Yandex API')
        elif not self.lineEdit_watcher_folder.text() or not os.path.isdir(self.lineEdit_watcher_folder.text()):
            QMessageBox.critical(self, 'Ошибка', 'Укажите папку с файлами для загрузки')
        elif not self.lineEdit_mail_server.text():
            QMessageBox.critical(self, 'Ошибка', 'Укажите адрес сервера')
        else:
            self.settings.setValue('first_run', False)
            self.settings.setValue('api_key', self.lineEdit_API.text())
            self.settings.setValue('folder', self.lineEdit_watcher_folder.text())
            self.settings.setValue('mail_error', self.lineEdit_mail_error.text())
            self.settings.setValue('mail_server', self.lineEdit_mail_server.text())
            self.settings_updated()

            super().accept()

    def settings_updated(self):
        settings = {}
        for key in self.settings.allKeys():
            settings[key] = self.settings.value(key)
        self.settings_dict.emit(settings)

    def exec(self):
        self.lineEdit_API.setText(self.getAPIKey())
        self.lineEdit_watcher_folder.setText(self.getFolder())
        self.lineEdit_mail_error.setText(self.getMailError())
        self.lineEdit_mail_server.setText(self.getMailServer())
        super().exec()