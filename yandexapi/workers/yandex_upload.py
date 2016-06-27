import logging
import os
import datetime
import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTime, QTimer
from yandexapi.api.yandex_api import YandexAPI


class WorkerYandexUpload(QObject):
    progress_bar = pyqtSignal(float)
    status = pyqtSignal(str)
    name = pyqtSignal(str)
    hide_progress_bar = pyqtSignal()
    set_icon = pyqtSignal(str)
    send_email = pyqtSignal(str, str, str)

    def __init__(self, file_path, api_key):
        super().__init__()
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.api = YandexAPI(api_key)
        self.bytes_read = 0
        self.file_size = os.path.getsize(self.file_path)
        # self.past_time = time.time()
        # self.time = QTime()
        # self.time.start()
        self.upload_start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.timer.setInterval(1000)

    def run(self):
        try:
            logging.debug('Обрабатываю файл: {}'.format(self.file_path))
            email_recipient = self.file_path.split('\\')[-2]

            self.name.emit('{} {}'.format(email_recipient, self.file_name))
            self.set_icon.emit(os.path.splitext(self.file_name)[1])
            file_object = None
            while file_object is None:
                try:
                    file_object = open(self.file_path, 'rb')
                except PermissionError:
                    time.sleep(1)
            # is user folder exist
            if self.api.is_path_exist('disk:/Загрузка/{}'.format(email_recipient)) is False:
                logging.debug('Folder is not exist')
                self.api.create_folder('disk:/Загрузка/{}'.format(email_recipient))
            # is file with same name exist
            if self.api.is_path_exist('disk:/Загрузка/{}/{}'.format(email_recipient, self.file_name)) is True:
                logging.debug('File is already exist')
                self.file_name = self.file_name.replace(self.file_name.split('.')[-2],
                                              self.file_name.split('.')[-2] +
                                              datetime.datetime.now().strftime('_%Y%m%d_%H-%M'))

            self.upload_start_time = datetime.datetime.now()
            self.api.upload_file(file_object, 'disk:/Загрузка/{}/{}'.format(email_recipient, self.file_name),
                                 self.upload_callback)

            file_object.close()
            self.timer.stop()
            self.hide_progress_bar.emit()
            self.status.emit('{} МБ — {}'.format(round(self.file_size / 1048576, 1),
                                                         self.upload_start_time.strftime('%d.%m %H:%M')))
            time.sleep(10)  # TODO Rewrite
            self.api.publish_file('disk:/Загрузка/{}/{}'.format(email_recipient, self.file_name))
            file_url = self.api.get_file_url('disk:/Загрузка/{}/{}'.format(email_recipient, self.file_name))
            logging.debug(file_url)
            html = self.generate_succesful_mail(self.file_name, file_url)
            self.send_email.emit(email_recipient, self.file_name, html)

        except Exception as e:
            logging.debug(e)

    def generate_succesful_mail(self, file_name, file_url):
        text = '''
        <html>
             <head>
                <style>
                body {{
                    font-family: Calibri,cursive;
                        }}
                a {{
                    text-decoration:none;
                    font-style:normal;
                    font-size:20px;
                    color:rgb(103, 143, 188);
                    }}
                .footer {{
                    font-size: 14px;
                    color: rgb(170, 170, 170);
                    font-style: italic;
                    }}
                </style>
            </head>
        <body>
            <p><span style="font-size: 16px; color:gray">Имя файла: {0}</span></p>
            <p><span style="font-size: 16px; color:gray">Ссылка для загрузки:</span></p>
            <a href={1}>{1}</a>
            <hr/>
            <span class="footer">Это сообщение было создано автоматически, <u>НЕ</u> нужно отвечать на него.</span>
        </body>
        </html>
        '''.format(file_name, file_url)
        return text


    @pyqtSlot()
    def update_speed(self):
        try:
            elapsed_time = (datetime.datetime.now() - self.upload_start_time).total_seconds()
            remaining_size = (self.file_size - self.bytes_read) / 1048576
            speed = round(self.bytes_read / 1048576 / elapsed_time, 2)
            remaining_time = round(remaining_size // speed)
            if 0 <= (remaining_time // 60) <= 60:
                minutes, seconds = divmod(remaining_time, 60)
                if minutes == 0:
                    remaining_time = '{} секунд'.format(seconds)
                else:
                    remaining_time = '{} минут и {} секунд'.format(minutes, seconds)
            else:
                minutes, seconds = divmod(remaining_time, 60)
                hours = minutes // 60
                if seconds == 0:
                    remaining_time = '{} часов и {} минут'.format(hours, minutes)
                else:
                    remaining_time = '{} часов, {} минут и {} cекунд'.format(hours, minutes, seconds)

            self.status.emit('Осталось {} — {} из {} МБ ({} МБ/сек)'.format(remaining_time,
                                                                                    self.bytes_read // 1048576,
                                                                                    self.file_size // 1048576,
                                                                                    speed))
        except (TypeError, ZeroDivisionError):  # TODO Timer won't start in run() method
            pass
        except Exception as e:
            logging.debug(e)

    # def upload_callback(self, file):
    #     try:
    #         self.progress_bar.emit(file.bytes_read * 100 / file.len)
    #         current_read = file.bytes_read
    #         current_time = time.time()
    #         logging.debug(current_read)
    #         logging.debug(current_read - self.bytes_read)
    #         send_bytes = current_read - self.bytes_read
    #         logging.debug(current_time - self.past_time)
    #         calc_time = current_time - self.past_time
    #         logging.debug(send_bytes / calc_time)
    #         speed = (send_bytes / calc_time) / 1024
    #         self.status.emit('{} килобайт/c'.format(speed))
    #         self.bytes_read = send_bytes
    #         self.past_time = current_time
    #     except Exception as e:
    #         logging.debug(e)

    def upload_callback(self, upload):
        self.bytes_read = upload.bytes_read
        self.progress_bar.emit(upload.bytes_read * 100 / upload.len)
