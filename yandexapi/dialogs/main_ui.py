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

        self.first_run()
        self.setup_top_menu()
        self.show()
        self.setup_worker_new_task()
        self.main_thread()

    def main_thread(self):
        logging.info('Запущен главный процесс')

    def add_list_widget_item(self):
        my_custom_widget = ItemListWidget()

        my_qlist_widget_item = QListWidgetItem()
        my_qlist_widget_item.setSizeHint(my_custom_widget.sizeHint())

        self.listWidget.insertItem(0, my_qlist_widget_item)
        self.listWidget.setItemWidget(my_qlist_widget_item, my_custom_widget)
        return my_qlist_widget_item


    def setup_top_menu(self):
        self.settings_menu.triggered.connect(self.settingsDialog.exec)
        self.quit_menu.triggered.connect(self.shutdown)

    def setup_worker_new_task(self):
        self.thread_new_task = QThread()
        self.worker_new_task = WorkerNewTask(self.settingsDialog.getFolder())

        self.worker_new_task.new_files.connect(self.start_pool_workers)
        self.worker_new_task.moveToThread(self.thread_new_task)
        self.thread_new_task.started.connect(self.worker_new_task.run)
        self.thread_new_task.start()

    @pyqtSlot(list)
    def start_pool_workers(self, files_list):
        try:
            for file in files_list:
                worker = WorkerYandexUpload(os.path.normpath(file), self.settingsDialog.getAPIKey())
                thread = QThread()

                listWidgetItem = self.add_list_widget_item()
                worker.progress_bar.connect(self.listWidget.itemWidget(listWidgetItem).set_progress)
                worker.name.connect(self.listWidget.itemWidget(listWidgetItem).set_name)
                worker.status.connect(self.listWidget.itemWidget(listWidgetItem).set_info)
                worker.hide_progress_bar.connect(self.listWidget.itemWidget(listWidgetItem).hide_progress)
                worker.set_icon.connect(self.listWidget.itemWidget(listWidgetItem).set_pixmap)
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

    def first_run(self):
        if self.settingsDialog.isFirstRun():
            if self.settingsDialog.exec() == QDialog.Rejected:
                sys.exit(0)  # TODO