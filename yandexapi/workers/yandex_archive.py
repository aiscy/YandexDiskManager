from PyQt5.QtCore import QObject


class WorkerYandexArchive(QObject):
    def __init__(self, ya_api):
        super().__init__()
        self.ya_api = ya_api