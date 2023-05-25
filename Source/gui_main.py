# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'UI/Main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets

from gui_news_component import NewsComponent
from gui_patch_viewer_component import PatchViewerComponent
from gui_common import ButtonLabel, MoveLabel


class MainWindowComponent:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.news_amount = 0
        self.jump_points = []
        self.news_components = []

        QtGui.QFontDatabase.addApplicationFont(':/Common/Play-Bold.ttf')
        QtGui.QFontDatabase.addApplicationFont(':/Common/PlayRegular-Regular.ttf')

    def setup_ui(self, main_window):
        main_window.setObjectName("Eternal Crusade: Resurrection")
        main_window.resize(960, 540)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        main_window.setMinimumSize(QtCore.QSize(960, 540))
        main_window.setMaximumSize(QtCore.QSize(960, 540))
        main_window.setAutoFillBackground(False)

        self.central_widget = QtWidgets.QWidget(main_window)

        self.main_screen_widget = QtWidgets.QWidget(self.central_widget)
        self.main_screen_widget.setStyleSheet("background-image: url(:/Common/Background.png);")
        self.main_screen_widget.setObjectName("main_screen_widget")

        self.patch_viewer = PatchViewerComponent(self.central_widget)
        self.patch_viewer.setGeometry(QtCore.QRect(0, 0, 960, 540))
        self.patch_viewer.setObjectName("patch_viewer")
        self.patch_viewer.setHidden(True)
        self.patch_viewer.setupUi()
        self.patch_viewer.CloseButton.clicked.connect(self.patch_viewer_closed_button_clicked)

        # Adding ability to drag the window
        self.movelabel = MoveLabel(self.central_widget, self)
        self.movelabel.setGeometry(QtCore.QRect(0, 0, 850, 50))
        self.movelabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.SizeAllCursor))
        self.movelabel.setText("")
        self.movelabel.setObjectName("movelabel")
        self.movelabel.raise_()

        # Defining main screen widget

        self.Logo = QtWidgets.QLabel(self.main_screen_widget)
        self.Logo.setGeometry(QtCore.QRect(30, 28, 201, 43))
        self.Logo.setAutoFillBackground(False)
        self.Logo.setStyleSheet("background: rgba(0, 0, 0, 0);")
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap(":/Common/Logo.png"))
        self.Logo.setObjectName("Logo")

        self.NewsLabel = ButtonLabel(self.main_screen_widget)
        self.NewsLabel.setGeometry(QtCore.QRect(40, 102, 41, 18))
        font = QtGui.QFont()
        font.setFamily("Play")
        font.setPointSize(12)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.NewsLabel.setFont(font)
        self.NewsLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.NewsLabel.setStyleSheet("QLabel {\n"
                                     "color: rgba(255, 255, 255, 225);\n"
                                     "background: rgba(0, 0, 0, 0);\n"
                                     "font-weight: bold;\n"
                                     "}\n"
                                     "\n"
                                     "QLabel::hover {\n"
                                     "color: rgba(255, 255, 255, 255);\n"
                                     "}")
        self.NewsLabel.setObjectName("NewsLabel")
        self.NewsLabel.clicked.connect(self.on_news_label_clicked)

        self.PatchNotesLabel = ButtonLabel(self.main_screen_widget)
        self.PatchNotesLabel.setGeometry(QtCore.QRect(95, 102, 100, 18))
        font = QtGui.QFont()
        font.setFamily("Play")
        font.setPointSize(11)
        font.setItalic(False)
        font.setWeight(75)
        self.PatchNotesLabel.setFont(font)
        self.PatchNotesLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.PatchNotesLabel.setStyleSheet("QLabel {\n"
                                           "color: rgba(255, 255, 255, 225);\n"
                                           "background: rgba(0, 0, 0, 0);\n"
                                           "font-weight: bold;\n"
                                           "}\n"
                                           "\n"
                                           "QLabel::hover {\n"
                                           "color: rgba(255, 255, 255, 255)\n"
                                           "}")
        self.PatchNotesLabel.setObjectName("PatchNotesLabel")
        self.PatchNotesLabel.clicked.connect(self.patch_notes_clicked)

        self.DiscordLabel = ButtonLabel(self.main_screen_widget)
        self.DiscordLabel.setGeometry(QtCore.QRect(213, 102, 70, 18))
        font = QtGui.QFont()
        font.setFamily("Play")
        font.setPointSize(11)
        font.setItalic(False)
        font.setWeight(75)
        self.DiscordLabel.setFont(font)
        self.DiscordLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DiscordLabel.setStyleSheet("QLabel {\n"
                                        "color: rgba(255, 255, 255, 225);\n"
                                        "background: rgba(0, 0, 0, 0);\n"
                                        "font-weight: bold;\n"
                                        "}\n"
                                        "\n"
                                        "QLabel::hover {\n"
                                        "color: rgba(255, 255, 255, 255)\n"
                                        "}")
        self.DiscordLabel.setObjectName("DiscordLabel")
        self.DiscordLabel.clicked.connect(self.on_discord_clicked)

        self.PBU = QtWidgets.QProgressBar(self.main_screen_widget)
        self.PBU.setGeometry(QtCore.QRect(0, 520, 960, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PBU.sizePolicy().hasHeightForWidth())
        self.PBU.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.PBU.setFont(font)
        self.PBU.setStyleSheet("QProgressBar {\n"
                               "    background-color: rgb(0, 0, 0);\n"
                               "    background: fill;\n"
                               "    border: 0;\n"
                               "}\n"
                               "\n"
                               "\n"
                               "QProgressBar::chunk {\n"
                               "    background-color: rgb(128, 0, 10);\n"
                               "}")
        self.PBU.setProperty("value", 0)
        self.PBU.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.PBU.setTextVisible(False)
        self.PBU.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.PBU.setInvertedAppearance(False)
        self.PBU.setObjectName("PBU")

        self.PlayButton = ButtonLabel(self.main_screen_widget, is_image=True,
                                      standard_image=":/Common/ButtonPlayActive.png",
                                      inactive_image=":/Common/ButtonPlayInactive.png",
                                      hovered_image=":/Hovered/ButtonPlayHovered.png",
                                      is_active_getter=self.is_play_button_active)
        self.PlayButton.setGeometry(QtCore.QRect(740, 462, 201, 41))
        self.PlayButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BusyCursor))
        self.PlayButton.setAutoFillBackground(False)
        self.PlayButton.setStyleSheet("QLabel {\n"
                                      "background: rgba(0, 0, 0, 0);\n"
                                      "}")
        self.PlayButton.setText("")
        self.PlayButton.setObjectName("PlayButton")
        self.PlayButton.clicked.connect(self.on_play_clicked)

        self.PBU_Status = QtWidgets.QLabel(self.main_screen_widget)
        self.PBU_Status.setGeometry(QtCore.QRect(10, 520, 700, 20))
        font = QtGui.QFont()
        font.setFamily("Play")
        font.setPointSize(8)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.PBU_Status.setFont(font)
        self.PBU_Status.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "background: rgba(0, 0, 0, 0);\n"
                                      "font-weight: bold;\n"
                                      "")
        self.PBU_Status.setObjectName("PBU_Status")

        self.PBU_Status_Speed = QtWidgets.QLabel(self.main_screen_widget)
        self.PBU_Status_Speed.setGeometry(QtCore.QRect(900, 520, 55, 20))
        font = QtGui.QFont()
        font.setFamily("Play")
        font.setPointSize(8)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.PBU_Status_Speed.setFont(font)
        self.PBU_Status_Speed.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "background: rgba(0, 0, 0, 0);\n"
                                            "font-weight: bold;\n"
                                            "")
        self.PBU_Status_Speed.setObjectName("PBU_Status_Speed")

        self.scrollArea = QtWidgets.QScrollArea(self.main_screen_widget)
        self.scrollArea.setGeometry(QtCore.QRect(40, 145, 920, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setStyleSheet("border: 0;\n"
                                      "background: rgba(0, 0, 0, 0);")
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.horizontalScrollBar().valueChanged.connect(self.on_news_scrolled)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1437, 284))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.CloseButton = ButtonLabel(self.main_screen_widget, is_image=True, standard_image=":/Common/ButtonExit.png",
                                       hovered_image=":/Hovered/ButtonExitHovered.png")
        self.CloseButton.setGeometry(QtCore.QRect(912, 24, 25, 25))
        self.CloseButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.CloseButton.setStyleSheet("background: rgba(0, 0, 0, 0);")
        self.CloseButton.setText("")
        self.CloseButton.setObjectName("CloseButton")
        self.CloseButton.clicked.connect(self.on_close_clicked)

        self.MinimizeButton = ButtonLabel(self.main_screen_widget, is_image=True,
                                          standard_image=":/Common/ButtonMinimize.png",
                                          hovered_image=":/Hovered/ButtonMinimizeHovered.png")
        self.MinimizeButton.setGeometry(QtCore.QRect(885, 29, 25, 25))
        self.MinimizeButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.MinimizeButton.setStyleSheet("background: rgba(0, 0, 0, 0);")
        self.MinimizeButton.setText("")
        self.MinimizeButton.setObjectName("MinimizeButton")
        self.MinimizeButton.clicked.connect(self.on_minimize_clicked)

        self.ButtonLeft = ButtonLabel(self.main_screen_widget, is_image=True, standard_image=":/Common/ButtonLeft.png",
                                      hovered_image=":/Hovered/ButtonLeftHovered.png")
        self.ButtonLeft.setGeometry(QtCore.QRect(10, 252, 51, 91))
        self.ButtonLeft.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ButtonLeft.setStyleSheet("background: rgba(0, 0, 0, 0);")
        self.ButtonLeft.setText("")
        self.ButtonLeft.setObjectName("ButtonLeft")
        self.ButtonLeft.setHidden(True)
        self.ButtonLeft.clicked.connect(self.show_news_previous)

        self.ButtonRight = ButtonLabel(self.main_screen_widget, is_image=True,
                                       standard_image=":/Common/ButtonRight.png",
                                       hovered_image=":/Hovered/ButtonRightHovered.png")
        self.ButtonRight.setGeometry(QtCore.QRect(900, 252, 51, 91))
        self.ButtonRight.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ButtonRight.setStyleSheet("background: rgba(0, 0, 0, 0);")
        self.ButtonRight.setText("")
        self.ButtonRight.setObjectName("ButtonRight")
        self.ButtonRight.clicked.connect(self.show_news_next)

        self.PBU.raise_()
        self.Logo.raise_()
        self.NewsLabel.raise_()
        self.PatchNotesLabel.raise_()
        self.DiscordLabel.raise_()
        self.PlayButton.raise_()
        self.PBU_Status.raise_()
        self.PBU_Status_Speed.raise_()
        self.scrollArea.raise_()
        self.CloseButton.raise_()
        self.MinimizeButton.raise_()
        self.ButtonRight.raise_()
        self.ButtonLeft.raise_()
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("main_window", "Eternal Crusade: Resurrection"))
        self.NewsLabel.setText(_translate("main_window", "SITE"))
        self.PatchNotesLabel.setText(_translate("main_window", "PATCH NOTES"))
        self.DiscordLabel.setText(_translate("main_window", "DISCORD"))
        self.PBU_Status.setText("")
        self.PBU_Status_Speed.setText("")

    def on_news_label_clicked(self):
        pass

    def patch_notes_clicked(self):
        self.patch_viewer.setVisible(True)

    def on_discord_clicked(self):
        pass

    def patch_viewer_closed_button_clicked(self):
        self.patch_viewer.setVisible(False)

    def on_minimize_clicked(self):
        pass

    def on_close_clicked(self):
        pass

    def on_play_clicked(self):
        pass

    def is_play_button_active(self):
        return True

    def update_buttons_visible(self):
        if self.scrollArea.horizontalScrollBar().value() == 0:
            self.ButtonLeft.setHidden(True)
        else:
            self.ButtonLeft.setHidden(False)

        if self.news_amount == 0:
            right_side = 0
        elif self.news_amount == 1:
            right_side = 0
        elif self.news_amount >= 2:
            right_side = 71 + 515 * (self.news_amount - 2)
        else:
            right_side = 0

        if self.scrollArea.horizontalScrollBar().value() >= right_side:
            self.ButtonRight.setHidden(True)
        else:
            self.ButtonRight.setHidden(False)

    def on_news_scrolled(self, event):
        self.update_buttons_visible()

    def show_news_previous(self):
        for i in reversed(range(1, len(self.jump_points))):
            left, right = self.jump_points[i - 1], self.jump_points[i]
            if left < self.scrollArea.horizontalScrollBar().value() <= right:
                self.scrollArea.horizontalScrollBar().setValue(left)
                break

    def show_news_next(self):
        for i in range(len(self.jump_points) - 1):
            left, right = self.jump_points[i], self.jump_points[i + 1]
            if left <= self.scrollArea.horizontalScrollBar().value() < right:
                self.scrollArea.horizontalScrollBar().setValue(right)
                break

    def add_news(self, is_first, news_piece):
        if not is_first:
            spacer = QtWidgets.QSpacerItem(33, 10)
            self.horizontalLayout_2.addItem(spacer)
            self.news_components.append(spacer)

        news = NewsComponent(self.scrollAreaWidgetContents)
        news.setupUi(news_piece["title"], news_piece["content"], news_piece["image"])
        self.horizontalLayout_2.addWidget(news)
        self.news_components.append(news)

    def refresh_news(self, news_data):
        if not isinstance(news_data, list):
            return

        self.news_amount = len(news_data)
        self.jump_points = [515 * i for i in range(self.news_amount + 1)]

        for i, piece in enumerate(news_data):
            self.add_news(i == 0, piece)

        self.update_buttons_visible()

    def refresh_status(self, status_text, status_speed_text=""):
        self.PBU_Status.setText(status_text)
        self.PBU_Status_Speed.setText(status_speed_text)

    def refresh_progress_bar(self, value):
        self.PBU.setValue(value)


import resources_rc
