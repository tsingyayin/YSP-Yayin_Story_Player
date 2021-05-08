

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.name = QLabel(self.centralwidget)
        self.name.setObjectName(u"name")
        self.name.setGeometry(QRect(110, 530, 72, 15))
        self.words = QLabel(self.centralwidget)
        self.words.setObjectName(u"words")
        self.words.setGeometry(QRect(240, 530, 72, 15))
        self.pic = QLabel(self.centralwidget)
        self.pic.setObjectName(u"pic")
        self.pic.setGeometry(QRect(90, 100, 72, 15))
        self.avg1 = QLabel(self.centralwidget)
        self.avg1.setObjectName(u"avg1")
        self.avg1.setGeometry(QRect(200, 250, 72, 15))
        self.avg2 = QLabel(self.centralwidget)
        self.avg2.setObjectName(u"avg2")
        self.avg2.setGeometry(QRect(340, 250, 72, 15))
        self.avg3 = QLabel(self.centralwidget)
        self.avg3.setObjectName(u"avg3")
        self.avg3.setGeometry(QRect(480, 250, 72, 15))
        self.freewords = QLabel(self.centralwidget)
        self.freewords.setObjectName(u"freewords")
        self.freewords.setGeometry(QRect(340, 210, 72, 15))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TESTWINDOW", None))
        self.name.setText("1")
        self.words.setText("2")
        self.pic.setText("4")
        self.avg1.setText("5")
        self.avg2.setText("6")
        self.avg3.setText("7")
        self.freewords.setText("8")
    # retranslateUi

