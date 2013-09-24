# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from app.static import icons

class Tab(QtGui.QWidget):

    ICON = "main"
    LABEL = "Tab"

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._setup_content()
        self._connect_events()

    def _setup_content(self):
        pass

    def _connect_events(self):
        pass

    def refresh(self):
        pass

    @classmethod
    def icon(cls):
        return QtGui.QIcon(icons[cls.ICON])
