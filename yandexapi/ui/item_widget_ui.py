# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'item_widget_ui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(353, 79)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setEnabled(True)
        self.label.setMaximumSize(QtCore.QSize(60, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/fileicon/file.png"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_name = QtWidgets.QLabel(Form)
        self.label_name.setText("")
        self.label_name.setObjectName("label_name")
        self.verticalLayout.addWidget(self.label_name)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.label_info = QtWidgets.QLabel(Form)
        self.label_info.setText("")
        self.label_info.setObjectName("label_info")
        self.verticalLayout.addWidget(self.label_info)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

import res_rc
