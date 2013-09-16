# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from app.static import icons

class Shuffle(QtGui.QMainWindow):
    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)
        
        self.app = app
        self.setWindowTitle("Desktop Shuffle")
        self.mainWidget=QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.setWindowIcon(QtGui.QIcon(icons['main']))
        self.setGeometry(350, 100, 620, 700)
        self.centralLayout=QtGui.QVBoxLayout(self.mainWidget)

        self.header=QtGui.QLabel("<h1>Desktop Shuffle</h1>")
        self.tab = QtGui.QToolBox(self.mainWidget)

        self.contextsWidget=QtGui.QWidget(self.tab)
        self.contextsLayout=QtGui.QGridLayout(self.contextsWidget)

        self.tab.addItem(app.newTab.setup_new(app, self), QtGui.QIcon(icons['new']), "New")
        self.tab.addItem(app.inboxTab.setup_inbox(app, self), QtGui.QIcon(icons['inbox']), "Inbox")
        self.tab.addItem(app.calendarTab.setup_calendar(app, self), QtGui.QIcon(icons['calendar']), "Calendar")
        self.tab.addItem(app.nextTab.setup_next(app, self), QtGui.QIcon(icons['next']), "Next actions")
        self.tab.addItem(app.projectTab.setup_projects(app, self), QtGui.QIcon(icons['projects']), "Projects")
        self.tab.addItem(app.contextTab.setup_contexts(app, self), QtGui.QIcon(icons['contexts']), "Contexts")
        self.tab.addItem(app.completeTab.setup_complete(app, self), QtGui.QIcon(icons['completed']), "Completed")
        self.tab.addItem(app.syncTab.setup_sync(app, self), QtGui.QIcon(icons['sync']), "Synchronization")

        self.centralLayout.addWidget(self.header)
        self.centralLayout.addWidget(self.tab)

        self.statusBar=QtGui.QStatusBar(self)
        self.statusBar.showMessage("Welcome", 2000)
        self.setStatusBar(self.statusBar)
        
    def closeEvent(self, event):
        #reply = QtGui.QMessageBox.question(self, 'Confirm Exit',"Are you sure to quit?", QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        #if reply == QtGui.QMessageBox.Yes:
        if self.app.inSync:
            event.ignore()
            QtGui.QMessageBox.information(self, "Abort", "You are in the middle of "
                                          + "a conflicted merge. Please resolve it first.")
        else:
            self.app.cursor.close()
            self.app.con.close()
            event.accept()
        #else:
        #    event.ignore()
        
