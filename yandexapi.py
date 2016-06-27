import logging
import os
import sys

from PyQt5.QtCore import QThread, QSettings, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QDialog, QFileDialog, QMessageBox, QListWidgetItem, QWidget
from PyQt5.QtGui import QPixmap

from yandexapi.ui.main_ui import Ui_MainWindow
# from yandexapi.ui.custom_widget import CustomWidget
from yandexapi.ui.item_widget_ui import Ui_Form
from yandexapi.ui.settings_ui import Ui_Dialog
from yandexapi.workers.new_task import WorkerNewTask
from yandexapi.workers.yandex_upload import WorkerYandexUpload
from yandexapi.email.smtp import SMTP
# from yandexapi.api.yandex_api import YandexAPI


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


class SettingsUI(QDialog, Ui_Dialog):
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

            super().accept()

    def exec(self):
        self.lineEdit_API.setText(self.getAPIKey())
        self.lineEdit_watcher_folder.setText(self.getFolder())
        self.lineEdit_mail_error.setText(self.getMailError())
        self.lineEdit_mail_server.setText(self.getMailServer())
        super().exec()


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.settingsDialog = SettingsUI()
        # self.tray = QSystemTrayIcon()
        # self.queue = queue.Queue()
        self.pool = []
        # self.smtp = SMTP(self.settingsDialog.getMailServer())  # TODO разлочить

        self.firstRun()
        self.setupTopMenu()
        self.show()
        self.setupWorkerNewTask()
        self.mainThread()

    def mainThread(self):
        logging.info('Запущен главный процесс')

    def addListWidgetItem(self):
        myCustomWidget = ItemListWidget()

        myQListWidgetItem = QListWidgetItem()
        myQListWidgetItem.setSizeHint(myCustomWidget.sizeHint())

        self.listWidget.insertItem(0, myQListWidgetItem)
        self.listWidget.setItemWidget(myQListWidgetItem, myCustomWidget)
        return myQListWidgetItem


    def setupTopMenu(self):
        self.settings_menu.triggered.connect(self.settingsDialog.exec)
        self.quit_menu.triggered.connect(self.shutdown)

    def setupWorkerNewTask(self):
        self.threadNewTask = QThread()
        self.workerNewTask = WorkerNewTask(self.settingsDialog.getFolder())

        self.workerNewTask.new_files.connect(self.startPoolWorkers)
        self.workerNewTask.moveToThread(self.threadNewTask)
        self.threadNewTask.started.connect(self.workerNewTask.run)
        self.threadNewTask.start()

    @pyqtSlot(list)
    def startPoolWorkers(self, files_list):
        try:
            for file in files_list:
                worker = WorkerYandexUpload(os.path.normpath(file), self.settingsDialog.getAPIKey())
                thread = QThread()

                listWidgetItem = self.addListWidgetItem()
                worker.progress_bar.connect(self.listWidget.itemWidget(listWidgetItem).setProgress)
                worker.name.connect(self.listWidget.itemWidget(listWidgetItem).setName)
                worker.status.connect(self.listWidget.itemWidget(listWidgetItem).setInfo)
                worker.hide_progress_bar.connect(self.listWidget.itemWidget(listWidgetItem).hideProgress)
                worker.set_icon.connect(self.listWidget.itemWidget(listWidgetItem).setPixmap)
                # worker.send_email.connect(self.send_mail)  # TODO разлочить

                worker.moveToThread(thread)
                thread.started.connect(worker.run)
                thread.start()

                logging.debug('Создан новый работник')
        except Exception as e:
            logging.debug(e)

    @pyqtSlot(str, str, str)
    def send_mail(self, email_recipient, subject, text):
        self.smtp.send_mail(email_recipient, subject, text)

    def shutdown(self):  # TODO
        qApp.quit()

    def firstRun(self):
        if self.settingsDialog.isFirstRun():
            if self.settingsDialog.exec() == QDialog.Rejected:
                sys.exit(0)  # TODO




if __name__ == '__main__':
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    app = QApplication(sys.argv)
    main_ui = MainUI()
    sys.exit(app.exec())
