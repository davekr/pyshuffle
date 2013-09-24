# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from app.static import icons
from app.tabs import New, Projects, Calendar, Inbox, Next, Contexts, Complete, Synchronization
import settings

class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self._setup_window()
        self._setup_content()
        self._setup_statusbar()

    def _setup_window(self):
        self.setWindowTitle("Desktop Shuffle")
        self.setWindowIcon(QtGui.QIcon(icons['main']))
        self.setGeometry(350, 100, 640, 740)

    def _setup_content(self):
        central_layout = self._setup_layout()
        main_widget = QtGui.QWidget()
        main_widget.setLayout(central_layout)
        self.setCentralWidget(main_widget)

    def _setup_layout(self):
        central_layout = QtGui.QVBoxLayout()
        header = QtGui.QLabel("<h1>Desktop Shuffle</h1>")
        central_layout.addWidget(header)
        toolbox = self._setup_tabs()
        central_layout.addWidget(toolbox)
        return central_layout

    def _setup_tabs(self):
        toolbox = QtGui.QToolBox()
        all_tabs = [New, Inbox, Calendar, Next, Projects, Contexts, Complete] #[, Synchronization]
        for tab in all_tabs:
            toolbox.addItem(tab(), tab.icon(), tab.LABEL)
        #toolbox.addItem(app.syncTab.setup_sync(app, self), QtGui.QIcon(icons['sync']), "Synchronization")
        return toolbox

    def _setup_statusbar(self):
        statusbar = QtGui.QStatusBar()
        self.setStatusBar(statusbar)
        self.show_status("Welcome")

    def show_status(self, status):
        """Shows message on application status bar"""
        self.statusBar().showMessage(status, 2000)

    def closeEvent(self, event):
        """Override the closeEvent method"""
        if settings.IN_SYNC:
            event.ignore()
            QtGui.QMessageBox.information(self, "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
        else:
            event.accept()
        
