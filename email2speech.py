# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from function import *
import pygame

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.function = email2speak()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(812, 495)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainMessage = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainMessage.setGeometry(QtCore.QRect(50, 180, 711, 181))
        self.plainMessage.setObjectName("plainMessage")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 153, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.stopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stopBtn.setGeometry(QtCore.QRect(290, 400, 111, 31))
        self.stopBtn.setObjectName("stopBtn")
        self.refreshBtn = QtWidgets.QPushButton(self.centralwidget)
        self.refreshBtn.setGeometry(QtCore.QRect(50, 400, 151, 31))
        self.refreshBtn.setObjectName("refreshBtn")
        self.plainFrom = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainFrom.setGeometry(QtCore.QRect(50, 90, 711, 31))
        self.plainFrom.setObjectName("plainFrom")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 811, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 60, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.replayBtn = QtWidgets.QPushButton(self.centralwidget)
        self.replayBtn.setGeometry(QtCore.QRect(650, 400, 111, 31))
        self.replayBtn.setObjectName("replayBtn")
        self.playBtn = QtWidgets.QPushButton(self.centralwidget)
        self.playBtn.setGeometry(QtCore.QRect(530, 400, 111, 31))
        self.playBtn.setObjectName("playBtn")
        self.pauseBtn = QtWidgets.QPushButton(self.centralwidget)
        self.pauseBtn.setGeometry(QtCore.QRect(410, 400, 111, 31))
        self.pauseBtn.setObjectName("pauseBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Email2Speech"))
        self.label_2.setText(_translate("MainWindow", "Message"))
        self.stopBtn.setText(_translate("MainWindow", "Stop"))
        self.refreshBtn.setText(_translate("MainWindow", "Get Message"))
        self.label.setText(_translate("MainWindow", "NLP - Email to Speech"))
        self.label_3.setText(_translate("MainWindow", "From"))
        self.replayBtn.setText(_translate("MainWindow", "Replay"))
        self.playBtn.setText(_translate("MainWindow", "Play"))
        self.pauseBtn.setText(_translate("MainWindow", "Pause"))

        self.refreshBtn.clicked.connect(self.getEmail)
        self.replayBtn.clicked.connect(self.audio_ctrl)
        self.stopBtn.clicked.connect(pygame.mixer.music.stop)
        self.pauseBtn.clicked.connect(pygame.mixer.music.pause)
        self.playBtn.clicked.connect(pygame.mixer.music.unpause)

    def getEmail(self):
        self.plainFrom.setReadOnly(False)
        self.plainFrom.setPlainText('')
        self.plainMessage.setReadOnly(False)
        self.plainMessage.setPlainText('')

        email = self.function.get_message()
        sender = self.function.get_sender()
        self.plainFrom.setPlainText(sender)
        self.plainFrom.setReadOnly(True)
        self.plainMessage.setPlainText(email)
        self.plainMessage.setReadOnly(True)

        self.function.save_audio()
        self.audio_ctrl()

    def audio_ctrl(self):
        self.function.play_audio()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
