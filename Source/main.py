import os
import sys
import ctypes

import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)
from PyQt6 import QtCore, QtGui

from gui_main import MainWindowComponent
from logic_supervisor import LogicSupervisor
from ecr_logging import log
from system_utils import is_windows_admin, rerun_as_windows_admin


class Window(QMainWindow, MainWindowComponent):
    def __init__(self, logic_supervisor, parent=None):
        super().__init__(parent)

        self.logic_supervisor: LogicSupervisor = logic_supervisor
        self.logic_supervisor.can_play_changed.connect(self.on_can_play_changed)
        self.logic_supervisor.status_changed.connect(self.on_status_changed)
        self.logic_supervisor.progress_changed.connect(self.on_progress_changed)
        self.logic_supervisor.launcher_update_needed.connect(self.on_launcher_update_needed)
        self.logic_supervisor.want_close.connect(self.on_close_clicked)

        self.setup_ui(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowTitleHint)
        self.setWindowIcon(QtGui.QIcon(':/Common/ECR_icon.ico'))

        if os.name == "nt":
            # Workaround for icon not shown on taskbar
            myappid = 'jediknightchannel.ecr.launcher.1'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Events, properties and signals

    def on_news_label_clicked(self):
        if self.logic_supervisor.site_link:
            self.logic_supervisor.open_internet_link(self.logic_supervisor.site_link)

    def on_discord_clicked(self):
        if self.logic_supervisor.discord_link:
            self.logic_supervisor.open_internet_link(self.logic_supervisor.discord_link)

    def on_close_clicked(self):
        if not self.logic_supervisor.get_can_exit():
            self.logic_supervisor.stop_requested = True
        QtCore.QCoreApplication.instance().quit()

    def on_minimize_clicked(self):
        self.showMinimized()

    def on_play_clicked(self):
        self.logic_supervisor.launch_game()

    def is_play_button_active(self):
        return self.logic_supervisor.get_can_play()

    def on_can_play_changed(self):
        self.PlayButton.manual_refresh()
        if self.logic_supervisor.get_can_play():
            self.PlayButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        else:
            self.PlayButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BusyCursor))

    def on_status_changed(self):
        self.refresh_status(self.logic_supervisor.get_status(), self.logic_supervisor.get_status_speed())

    def on_progress_changed(self):
        self.update()
        self.refresh_progress_bar(self.logic_supervisor.get_progress())

    def on_launcher_update_needed(self):
        log("Starting launcher update process")

        if os.name == "nt":
            cmd = "launcher_updater.exe"
        else:
            cmd = None

        # Check if there is executable
        if cmd and not os.path.exists(cmd):
            cmd = None

        if cmd:
            self.logic_supervisor.run_detached_process(cmd)

        self.on_close_clicked()

    # Main actions

    def refresh_news_and_patch_notes(self):
        patch_notes = self.logic_supervisor.get_patch_notes()
        self.patch_viewer.refresh_patch_notes(patch_notes)

        news_data = self.logic_supervisor.get_news()
        self.refresh_news(news_data)

    def verify_and_check_for_game_updates(self):
        self.logic_supervisor.verify_and_check_for_updates()


if __name__ == "__main__":
    if os.name == "nt":
        # Require admin rights
        if not is_windows_admin():
            rerun_as_windows_admin()

    # os.environ.setdefault("QT_DEBUG_PLUGINS", "1")
    logic_supervisor_main = LogicSupervisor()

    app = QApplication(sys.argv)
    win = Window(logic_supervisor_main)
    win.refresh_news_and_patch_notes()
    win.show()

    win.verify_and_check_for_game_updates()

    sys.exit(app.exec())
