import logging
import os
import sys

from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, qApp, QDialog

from yandexapi.dialogs.item_list_widget import ItemListWidget
from yandexapi.dialogs.settings_ui import SettingsUI
from yandexapi.ui.main_ui import Ui_MainWindow
from yandexapi.workers.new_task import WorkerNewTask
from yandexapi.workers.yandex_upload import WorkerYandexUpload


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