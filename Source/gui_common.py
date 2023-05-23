from PyQt6.QtWidgets import QLabel, QDialog, QPushButton
from PyQt6.QtCore import pyqtSignal, QEvent
from PyQt6 import QtGui

import numpy as np


class ButtonLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, is_image=False, standard_image=None, inactive_image=None, hovered_image=None,
                 is_active_getter=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_image = is_image
        self.is_active_getter = is_active_getter

        if is_image:
            self.installEventFilter(self)
            self.standard_image = standard_image
            self.inactive_image = inactive_image
            self.hovered_image = hovered_image

        self.manual_refresh()

    def manual_refresh(self):
        if self.is_image:
            if not self.is_active_getter or self.is_active_getter():
                self.setPixmap(QtGui.QPixmap(self.standard_image))
            else:
                self.setPixmap(QtGui.QPixmap(self.inactive_image))

    def mousePressEvent(self, ev):
        if not self.is_active_getter or self.is_active_getter():
            self.clicked.emit()

    def eventFilter(self, object, event):
        if event.type() == QEvent.Type.Enter:
            self.on_mouse_enter()
            return True
        elif event.type() == QEvent.Type.Leave:
            self.on_mouse_leave()
            return True
        return False

    def on_mouse_enter(self):
        if self.is_image and (not self.is_active_getter or self.is_active_getter()):
            self.setPixmap(QtGui.QPixmap(self.hovered_image))
        pass

    def on_mouse_leave(self):
        if self.is_image:
            if not self.is_active_getter or self.is_active_getter():
                self.setPixmap(QtGui.QPixmap(self.standard_image))
            else:
                self.setPixmap(QtGui.QPixmap(self.inactive_image))
        pass


# A label used to move a window - moving_obj parameter
class MoveLabel(QLabel):
    def __init__(self, frame, moving_obj):
        super().__init__(frame)
        self.moving_obj = moving_obj
        self.offset = None

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalPosition().x()
        y = event.globalPosition().y()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.x = x - x_w
        self.y = y - y_w
        self.moving_obj.move(self.x, self.y)


def pixmap_to_array(pixmap):
    size = pixmap.size()
    h = size.width()
    w = size.height()

    qimg = pixmap.toImage()
    s = qimg.bits().asstring(w * h * 4)
    arr = np.fromstring(s, dtype=np.uint8).reshape((w, h, 4))
    return arr
