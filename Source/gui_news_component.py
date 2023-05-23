# -*- coding: utf-8 -*-
import random

# self implementation generated from reading ui file 'UI/NewsComponent.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets

from gui_common import pixmap_to_array
from image_generator import get_image


class NewsComponent(QtWidgets.QWidget):
    def setupUi(self, title_text, content_text, background):
        self.setObjectName("self")

        self.setMinimumSize(QtCore.QSize(476, 284))
        self.setMaximumSize(QtCore.QSize(476, 284))

        self.resize(476, 284)

        self.Background = QtWidgets.QLabel(self)
        self.Background.setGeometry(QtCore.QRect(0, 0, 476, 284))
        self.Background.setText("")

        frame = QtGui.QPixmap(":/Common/NewsFrame.png")
        frame = pixmap_to_array(frame)

        mask = QtGui.QPixmap(":/Common/NewsMask.png")
        mask = pixmap_to_array(mask)

        news_image = QtGui.QPixmap()
        news_image.loadFromData(QtCore.QByteArray.fromBase64(get_image(frame, mask, background)))

        self.Background.setPixmap(news_image)
        self.Background.setObjectName("Background")

        self.Title = QtWidgets.QLabel(self)
        self.Title.setGeometry(QtCore.QRect(35, 207, 421, 17))
        font = QtGui.QFont()
        font.setFamily("Play")
        font.setPointSize(15)
        font.setWeight(75)
        self.Title.setFont(font)
        self.Title.setStyleSheet("color: rgb(255, 255, 255); background: rgba(0, 0, 0, 0); font-weight: bold;")
        self.Title.setObjectName("Title")
        self.Title.setText(title_text)

        self.Text = QtWidgets.QLabel(self)
        self.Text.setGeometry(QtCore.QRect(35, 235, 421, 31))
        font = QtGui.QFont()
        font.setFamily("Play Regular")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Text.setFont(font)
        self.Text.setStyleSheet("color: rgb(255, 255, 255); background: rgba(0, 0, 0, 0);")
        self.Text.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.Text.setWordWrap(True)
        self.Text.setObjectName("Text")
        self.Text.setText(content_text)
        self.Text.setOpenExternalLinks(True)

        QtCore.QMetaObject.connectSlotsByName(self)
