import os
from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal


class WorkerNewTask(QObject):
    new_files = pyqtSignal(list)

    def __init__(self, root_path):
        super().__init__()
        self.root_path = root_path

    def files_list(self):  # TODO rewrite
        matches = []
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if file.endswith(('.zip', '.rar', '.7z')):
                    matches.append(os.path.join(root, file))
        return matches

    def run(self):
        files_before = self.files_list()
        while True:
            sleep(10)
            files_after = self.files_list()
            added_files = list(set(files_after).difference(files_before))
            if added_files:
                self.new_files.emit(added_files)
            files_before = files_after