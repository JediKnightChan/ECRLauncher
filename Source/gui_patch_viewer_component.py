# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'UI/PatchViewerComponent.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets

from gui_common import ButtonLabel


class PatchViewerComponent(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dynamic_components = []

    def setupUi(self):
        self.resize(960, 540)
        self.setMinimumSize(QtCore.QSize(960, 540))
        self.setMaximumSize(QtCore.QSize(960, 540))

        self.Background = QtWidgets.QLabel(self)
        self.Background.setGeometry(QtCore.QRect(0, 0, 960, 540))
        self.Background.setStyleSheet("background-color: rgba(0, 0, 0, 225);")
        self.Background.setText("")
        self.Background.setObjectName("Background")

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setGeometry(QtCore.QRect(30, 50, 900, 440))
        self.scrollArea.setStyleSheet("QScrollArea { background: transparent; border: 0; }\n"
                                      "QScrollArea > QWidget > QWidget { background: transparent; }\n"
                                      "\n"
                                      "QScrollBar:vertical {\n"
                                      "    width: 4px;\n"
                                      "    margin: 0px 0px 0px 0px;\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar::handle:vertical {\n"
                                      "    min-height: 0px;\n"
                                      "    border-radius: 2px;\n"
                                      "    background: white;\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar::add-line:vertical {\n"
                                      "    height: 0px;\n"
                                      "    subcontrol-position: bottom;\n"
                                      "    subcontrol-origin: margin;\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar::sub-line:vertical {\n"
                                      "    height: 0px;\n"
                                      "    subcontrol-position: top;\n"
                                      "    subcontrol-origin: margin;\n"
                                      "}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 894, 599))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 30, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.CloseButton = ButtonLabel(self, is_image=True, standard_image=":/Common/ButtonClosePatch.png",
                                       hovered_image=":/Hovered/ButtonClosePatchHovered.png")
        self.CloseButton.setGeometry(QtCore.QRect(914, 19, 21, 21))
        self.CloseButton.setText("")
        self.CloseButton.setPixmap(QtGui.QPixmap())
        self.CloseButton.setObjectName("CloseButton")
        self.CloseButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.CloseButton.manual_refresh()

        QtCore.QMetaObject.connectSlotsByName(self)

    def add_header(self, text):
        header = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Play")
        font.setPointSize(16)
        font.setWeight(75)
        header.setFont(font)
        header.setStyleSheet("color: rgb(255, 255, 255); font-weight: bold;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        header.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(header)
        header.setText(text)

        self.dynamic_components.append(header)

    def add_paragraph(self, text):
        label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Play Regular")
        label.setFont(font)
        label.setStyleSheet("color: rgb(255, 255, 255);")
        label.setWordWrap(True)
        self.verticalLayout.addWidget(label)

        label.setText(text)
        label.setOpenExternalLinks(True)
        self.dynamic_components.append(label)

    def add_spacer(self, height):
        spacer = QtWidgets.QSpacerItem(10, height)
        self.verticalLayout.addItem(spacer)

        self.dynamic_components.append(spacer)

    def refresh_patch_notes(self, patch_notes):
        for comp in self.dynamic_components:
            if isinstance(comp, QtWidgets.QWidget):
                self.verticalLayout.removeWidget(comp)
                comp.setParent(None)
            else:
                self.verticalLayout.removeItem(comp)

        for patch_note in patch_notes:
            self.add_header(patch_note["title"])
            self.add_spacer(20)
            self.add_paragraph(patch_note["content"])
            self.add_spacer(50)
