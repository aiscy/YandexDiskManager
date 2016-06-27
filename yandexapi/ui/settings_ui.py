# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_ui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.setEnabled(True)
        Dialog.resize(550, 169)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/slowpoke.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.lineEdit_mail_error = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_mail_error.setObjectName("lineEdit_mail_error")
        self.gridLayout.addWidget(self.lineEdit_mail_error, 4, 2, 1, 1)
        self.lineEdit_API = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_API.setObjectName("lineEdit_API")
        self.gridLayout.addWidget(self.lineEdit_API, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 8, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 2, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_watcher_folder = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_watcher_folder.setObjectName("lineEdit_watcher_folder")
        self.gridLayout_2.addWidget(self.lineEdit_watcher_folder, 0, 1, 1, 1)
        self.toolButton = QtWidgets.QToolButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.toolButton.setFont(font)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_2.addWidget(self.toolButton, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 2, 2, 2, 1)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 2, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.lineEdit_mail_server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_mail_server.setObjectName("lineEdit_mail_server")
        self.gridLayout.addWidget(self.lineEdit_mail_server, 5, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.lineEdit_API.textChanged['QString'].connect(self.label_2.setText)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEdit_API, self.lineEdit_mail_error)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Настройки"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">API ключ</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog", "Адрес для отчета об ошибках"))
        self.label_2.setText(_translate("Dialog", "Настройки применяются только после перезапуска."))
        self.toolButton.setText(_translate("Dialog", "Обзор..."))
        self.label.setText(_translate("Dialog", "Папка для отслеживания"))
        self.label_3.setText(_translate("Dialog", "Адрес почтового сервера"))

import res_rc
